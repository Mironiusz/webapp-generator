# Jak działa ten config

## Wprowadzenie

Często można spotkać się z plikiem konfiguracyjnym ze stałymi konfiguracyjnymi, które czytają coś z .env:

```python
from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
```

Takie podejście ma kilka wad:

- Nic nie chroni SECRET_KEY przed byciem wyświetlonym,
- Zupełny brak walidacji LOG_LEVEL, czy ma poprawną wartość,
- getenv czyta tylko zmienne systemowe i w ogóle nie obsługuje plików .env,
- Każda wartość przychodzi jako string, więc liczby i boole trzeba konwertować ręcznie,
- Grupowanie stałych konfiguracyjnych tylko poprzez formatowanie pliku.

I oczywiście, tę ochronę, walidację, ścieżki można dodawać samemu. To jednak wymaga albo dopisania dodatkowej biblioteki, albo zmiany wygodnego pliku konfiguracyjnego w moduł. Co jest bez sensu i tylko zmniejsza czytelność.

Warto więc korzystać z takiej konfiguracji, która spełni od razu kilka założeń:

- Nie wymaga pisania własnej walidacji,
- Chroni secrety przed wyciekiem,
- Pozwala na łatwe korzystanie z kilku plików .env,
- Pozwala na ustawienie wartości domyślnej, nadpisywalnej przez .env,
- Natywnie pogrupuje stałe konfiguracyjne.

Na to właśnie pozwala użyty w tym pliku konfiguracyjnym `pydantic_settings`.

## Jak to działa

W jakimś pliku korzystającym z konfiguracji, importujemy ustawienia:

```python
from app.core.config import get_settings

settings = get_settings()

api_version = settings.api.version
secret_key = settings.secret_key.get_secret_value()
```

Przy imporcie modułu powstaje sama klasa Settings - pydantic czyta wtedy jej pola i model_config, ale niczego jeszcze nie wczytuje. Dopiero `get_settings()` tworzy instancję i to jest moment, w którym silnik sięga do środowiska.

BaseSettings i dziedziczące po niej klasy mają pewną konwencję: dla każdego swojego pola szukają zmiennej o tej samej nazwie - najpierw wśród zmiennych systemowych, potem w plikach środowiskowych.

To, na jakiej zasadzie klasa będzie szukać, wynika ze słownika model_config, będącego instancją `SettingsConfigDict`. Silnik dowiaduje się, że ma szukać tylko w plikach zdefiniowanych w env_file, czyli w naszym wypadku .env i .env.local, kodować je w utf-8, nie być case sensitive, odrzucać nadmiarowe klucze i być niemutowalny. Pliki czytane są po kolei i przy konflikcie wygrywa ostatni, czyli .env.local - dlatego sekrety trzymamy w .env, a ustawienia konkretnej maszyny w .env.local. Brakujący plik jest po prostu pomijany.

Mamy extra=forbid - gdy w envie są zmienne niewymienione w klasie jako pole, rzuca błąd. Gdyby było extra=ignore, dodatkowe zmienne byłyby ignorowane, a extra=allow dodałoby je automatycznie. Dotyczy to zawartości plików .env, bo innych zmiennych systemowych silnik nie ogląda.

Jest też delimiter `__` - on pozwala w envie nadpisywać drzewiaste wartości z konfiguracji. Mając wewnątrz klasy `Settings database: DatabaseSettings = DatabaseSettings()`, pod `settings.database` mamy gotową instancję sekcji ze wszystkimi jej polami. Jeśli chcemy któreś nadpisać, wystarczy w .env dodać na przykład `DATABASE__URL`, i już to samo nadpisze `settings.database.url`. Działa to na poszczególnych polach, więc reszta sekcji pozostanie z wartościami domyślnymi.

Sekcje dziedziczą po SettingsSection, by extra i frozen działały wewnątrz nich. Dzięki temu zmienne po danym delimiterze też są weryfikowane, i na przykład `DATABASE__URLL` nie przejdzie.

SECRET_KEY jest typu SecretStr, więc nie da się go wypisać przez przypadek, dopóki nie użyjemy jawnej metody get_secret_value().

Na koniec jest model_validator. Dostaje gotowy, zwalidowany obiekt, więc widzi wszystkie pola jednocześnie i pilnuje reguł, które wolno złamać lokalnie, ale nie na produkcji.

Samo get_settings() jest opakowane w lru_cache, więc Settings jest singletonem, a środowisko czytane jest raz na proces.
