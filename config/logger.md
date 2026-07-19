## Specyfikacja loggera

- Logger ma bazową nazwę aplikacji, `generator`.

- Moduł loggera nazywa się `logger`

- System ma mieć jeden logger nadrzędny aplikacji.

- Każdy moduł tworzy logger na podstawie `__name__`.

- Nazwa loggera ma odzwierciedlać strukturę modułów, np.:
    - `generator`
    - `generator.fleethand`
    - `generator.fleethand.tasks`
    - `generator.database.export`

- Konfiguracja loggera jest wykonywana tylko raz podczas startu aplikacji.

- Pobranie loggera nie może automatycznie konfigurować całego systemu.

- Poziomy powinny być przekazywane jako wartości `logger.DEBUG`, `logger.INFO` itd., a nie jako dowolne stringi.

- Niepoprawna konfiguracja nie powinna być cicho zastępowana wartością domyślną.

- Konsola domyślnie pokazuje logi od poziomu `DEBUG`.

- Plik domyślnie zapisuje logi od poziomu `DEBUG`.

- Oba poziomy regulowane w pliku `/config/config.py`

- Logger zapisuje logi jednocześnie:
    - do konsoli,
    - do jednego pliku.

- Domyślna ścieżka pliku to:

```text
log/generator.log
```

- Folder na logi jest tworzony automatycznie, jeśli nie istnieje.

- Kodowanie pliku to UTF-8.

- Plik logów jest czyszczony przy każdym uruchomieniu aplikacji.

- System nie tworzy:
    - plików historycznych,
    - rotacji dziennej,
    - rotacji tygodniowej,
    - osobnych plików debug,
    - osobnych folderów dla grup loggerów.

- Format logu zawiera:
    - datę i czas,
    - poziom logu,
    - pełną nazwę loggera,
    - treść komunikatu.

- Przykładowy format:

```text
2026-07-19 12:30:15 | INFO | generator.fleethand.tasks | Rozpoczynam przetwarzanie zadań
```

- Logi `DEBUG` muszą dodatkowo zawierać numer linii i nazwę funkcji w formacie:

```text
2026-07-19 12:30:15 | INFO | generator.fleethand.tasks: generate_tasks: 317 | Rozpoczynam generowanie tasków
```

- Jeden format dla konsoli i pliku.

- Dodajemy kolorowanie konsoli od razu

- Loggery modułów nie mają własnych handlerów.

- Logi z modułów propagują do loggera nadrzędnego.

- Logger nie powinien przechwytywać wszystkich zewnętrznych bibliotek przez root logger.

- Zewnętrzne biblioteki pozostają poza przestrzenią nazw `generator`.

- Ponowne wywołanie konfiguracji nie może dodawać kolejnych identycznych handlerów.

- Konfiguracja loggera nie powinna modyfikować globalnie `stdout` ani `stderr`.

- Logger powinien poprawnie obsługiwać:
    - `debug`,
    - `info`,
    - `warning`,
    - `error`,
    - `critical`,
    - `exception`.

- Wyjątki logujemy przez `logger.exception()` wewnątrz bloku `except`.

- Dane przekazujemy do loggera przez argumenty:

```python
logger.info("Przetworzono %s rekordów", record_count)
```

- Nie budujemy domyślnie komunikatów przez f-stringi, jeśli mogą zawierać kosztowne obliczenia.

## Poza tą wersją iteracja

- JSON logs,
- rotacja plików,
- kompresowanie logów,
- osobne pliki dla modułów,
- wysyłanie logów do zewnętrznych systemów,
- asynchroniczne logowanie,
- kontekst requestów i correlation ID,
- automatyczne przekierowanie logów bibliotek zewnętrznych.
