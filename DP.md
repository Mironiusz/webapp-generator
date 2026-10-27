# SDI - Duża Prezentacja

## Tytuł

Generator szkieletów aplikacji webowych

Rafał Mironko, Informatyka, Inżynieria Oprogramowania

Opiekun: dr Szymon Kijas, IAiIS

## Plan prezentacji (1min)

- Omówienie problemu
- Cel pracy i efekt dla użytkownika
- Opis oczekiwanego działania
- Specyfikacja
- Kluczowe decyzje projektowe i założenia architektoniczne
- Ryzyka projektowe
- Architektura
- Dotychczasowe wyniki pracy
- Plan prac na ten semestr i program minimum

## Omówienie problemu (2min)

Wielu programistów doskonale potrafi rozszerzać i edytować aplikacje webowe. Gorzej, kiedy trzeba postawić nową. Sam wiele razy musiałem stawiać nowy projekt i za każdym razem kończyło się to tak samo: za każdym razem pisałem niemal identyczny boilerplate'owy kod i wykonywałem niemal identyczne procedury, lub po prostu kopiowałem i okrajałem stary projekt. Oba podejścia mają wady: duża strata czasu lub mniejsza strata czasu z ryzykiem pomyłki, pozostawieniem czegoś, co nie powinno się znakleźć w repo oraz narzucenie sobie starej, nieaktualizowanej struktury.

Samo postawienie projektu od nowa zwykle wymaga sięgnięcia do dokumentacji, żeby:

- poprawnie zainicjalizować projekt frontendu
- napisać podstawowy routing
- zainstalować odpowiednie pakiety
- połączyć frontend z backendem bez problemów z CORS
- stworzyć Dockerfile, który od razu zadziała

Do tego dochodzą elementy, które ma prawie każda aplikacja:

- rejestracja i logowanie z obsługą tokenów JWT
- migracje bazy danych
- testy
- healthchecki

Problematyczne dla początkujących jest też pilnowanie od początku standardów i konwencji oraz pisanie aplikacji gotowej do testowania na docelowej infrastrukturze.

Do tego to wszystko po prostu zabiera czas, nieważne, jak dobry programista by nie był. Dlatego postanowiłem stworzyć generator szkieletów aplikacji webowych, który wszystkie te nieprzyjemne, boilerplate'owe kroki wykona za użytkownika.

## Cel pracy i efekt dla użytkownika (2min)

Celem projektu jest zaprojektowanie i implementacja narzędzia CLI generującego konteneryzowane szkielety aplikacji webowych na podstawie kreatora lub pliku konfiguracyjnego. Generator ma ograniczyć ilość powtarzalnej pracy potrzebnej do uruchomienia nowej aplikacji oraz zapewnić spójny, testowalny i rozszerzalny punkt startowy dla dalszego rozwoju projektu.

Po przejściu przez kreator aplikacji lub uruchomieniu generatora z plikiem konfiguracyjnym powstaje działający, konteneryzowany szkielet aplikacji webowej z konfiguracją środowiskową, który wystarczy rozszerzać i modyfikować.

## Opis oczekiwanego działania

- użytkownik uruchamia kreator albo wskazuje plik konfiguracyjny
- wybiera lub deklaruje frontend (Nuxt, opcjonalnie React)
- wybiera lub deklaruje backend-db stack (FastAPI + SQLite oraz drugi stack z PostgreSQL: ASP.NET Core albo Django)

Następnie generator tworzy projekt, weryfikuje go testami i dopiero wtedy zapisuje w katalogu docelowym.

## Specyfikacja

### Tryby działania

1. Tryb kreatora

Użytkownik odpowiada na pytania i podejmuje decyzje:

- nazwa projektu
- katalog docelowy
- frontend
- backend-db stack
- porty albo wartości domyślne
- zmienne środowiskowe albo wartości domyślne

2. Tryb pliku konfiguracyjnego

Generator przyjmuje plik konfiguracyjny w formacie YAML i działa bez jakiejkolwiek interakcji. Jeśli katalog docelowy nie jest pusty, generator przerywa działanie, chyba że uruchomiono go z flagą -f.

### Wspierane technologie i kombinacje

Pierwotna specyfikacja zakłada cztery kombinacje:

- Nuxt + FastAPI + SQLite
- React + FastAPI + SQLite
- Nuxt + Django + PostgreSQL
- React + Django + PostgreSQL

Generator w tej wersji nie musi obsługiwać kombinacji spoza tej listy, ale musi być rozszerzalny o nowe frameworki frontendowe i backendowe.

Planowane zmiany względem specyfikacji:

- React prawdopodobnie powstanie w wersji okrojonej, głównie o testy i obsługę błędów. Nadal będzie spełniał kontrakt API, więc zadziała z oboma backend-db stackami.
- Drugim backend-db stackiem może zostać ASP.NET Core + PostgreSQL zamiast Django + PostgreSQL. Backend spoza ekosystemu Pythona lepiej sprawdza, czy rozszerzanie generatora rzeczywiście nie zależy od technologii. Jeśli zabraknie czasu, zostaje Django + PostgreSQL, które korzysta z istniejącej infrastruktury dla Pythona.

Decyzję podejmę najpóźniej do końca listopada. Priorytetem jest zapas czasu na dokończenie generatora i napisanie pracy, nawet kosztem okrojonego Reacta i pozostania przy Django.

### Wymagania funkcjonalne generatora

- Generator musi umożliwiać utworzenie projektu na podstawie kreatora.
- Generator musi umożliwiać utworzenie projektu na podstawie pliku konfiguracyjnego.
- Generator musi walidować konfigurację przed rozpoczęciem generacji.
- Generator musi wykrywać niewspierane kombinacje technologiczne.
- Generator musi wykrywać konflikty portów.
- Generator musi zweryfikować wygenerowany projekt testami przed zapisem w katalogu docelowym.
- Generator musi utworzyć projekt w katalogu docelowym.
- Generator musi raportować czas generacji i podstawowe statystyki.
- Generator może umożliwiać wznowienie generacji po błędzie. Zmiana względem specyfikacji: wymaganie jest opcjonalne i powstanie, jeśli wystarczy czasu.

Generator musi przerwać działanie przed rozpoczęciem generacji, jeśli:

- wybrano niewspieraną kombinację technologii
- brakuje wymaganych danych wejściowych
- wskazany katalog docelowy jest niepoprawny
- porty wymagane przez usługi są skonfliktowane
- zmienne środowiskowe są niepoprawne

### Wymagania funkcjonalne wygenerowanej aplikacji

1. Frontend

- routing
- strona logowania
- strona rejestracji
- strona aplikacji, dostępna po zalogowaniu
- strona 404
- klient HTTP do backendu
- obsługa tokena JWT
- obsługa błędu logowania
- testy jednostkowe
- testy integracyjne

2. Backend

- endpointy stanu: `GET /health`, `GET /health/db`, `GET /health/ready`
- rejestracja: `POST /api/v1/auth/register`
- logowanie: `POST /api/v1/auth/login`
- dane aktualnego użytkownika: `GET /api/v1/auth/me`
- obsługa CORS
- obsługa JWT
- testy jednostkowe
- testy integracyjne

3. Baza danych

Baza danych jest w PostgreSQL lub w SQLite.

Backend zapewnia:

- migracje
- minimalny model użytkownika
- strukturę danych wymaganą do działania podstawowego mechanizmu uwierzytelniania

4. Komunikacja

- działa komunikacja frontend-backend
- działa komunikacja backend-db

"Działanie" definiuję przejściem testów integracyjnych oraz testu dymnego happy path: rejestracja -> logowanie -> pobranie danych użytkownika.

### Kontrakt danych

Minimalny model użytkownika musi pozwalać na:

- jednoznaczną identyfikację użytkownika
- logowanie za pomocą emaila
- rejestrację za pomocą emaila
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

Kontrakt danych nie wymaga identycznej fizycznej struktury wszystkich tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez framework.

### Wymagania niefunkcjonalne

1. Idempotentność

Ponowne uruchomienie generatora dla tej samej konfiguracji prowadzi do tej samej struktury projektu i nie może prowadzić do niespójnego lub częściowo uszkodzonego wyniku. Nieudana generacja nie zostawia pozostałości w katalogu docelowym.

2. Deterministyczność

Dla tej samej konfiguracji generator powinien tworzyć taki sam wynik strukturalny, poza losowanymi sekretami.

3. Rozszerzalność

Dodanie nowego frontendu albo backendu nie powinno wymagać modyfikacji istniejących wspieranych kombinacji technologicznych.

4. Niezależność wygenerowanego projektu od generatora

Wygenerowany projekt musi być możliwy do uruchomienia bez generatora.

5. Jakość wygenerowanego projektu

Wygenerowany projekt musi spełniać szeroko pojęte dobre praktyki programistyczne, między innymi:

- zasady SOLID
- zasada DRY
- testy jednostkowe dla kluczowych elementów backendu i frontendu
- testy integracyjne potwierdzające działającą komunikację frontend-backend oraz backend-db
- samodokumentujący się, czytelny kod z docstringami funkcji, ale bez komentarzy linijkowych
- pliki dokumentacyjne informujące, jak rozszerzać moduły i zgodnie z jakimi standardami zostały one stworzone

Jakość jest sprawdzana automatycznie narzędziami jakości (lint, formatowanie, typy) i testami.

Projekt ma być łatwy do rozszerzenia dla użytkownika generatora, bez konieczności tworzenia zupełnie nowych modułów i wprowadzania nowych standardów.

## Kluczowe decyzje projektowe i założenia architektoniczne

1. Frontend zależy wyłącznie od kontraktu HTTP API

   Frontend nie wie nic o tym, jaki backend został wybrany. Dla frontendu istotne jest jedynie to, żeby backend wystawiał mu określone endpointy. Dzięki temu rozszerzanie generatora o kolejny frontend sprowadza się do napisania frontendu zgodnego z kontraktem API. Frontend pełni bowiem rolę warstwy prezentacji oraz klienta korzystającego z publicznego API backendu.

2. Backend i baza danych traktowane są jako backend-db stack

   Być może na papierze wygodne byłoby rozdzielenie backendu i bazy danych, żeby tworzyć dowolne kombinacje. Niestety, backend ma zbyt duży wpływ na sposób działania bazy danych:
   - ORM
   - migracje
   - modele
   - auth
   - struktura danych wymagana do uwierzytelniania
   - tabele techniczne
   - testy backend-db

   To wszystko sprawia, że obsługa takiej macierzy kombinacji szybko stałaby się nienatywna i pełna sztucznych warunków. Stąd decyzja o utrzymaniu backendu i bazy danych jako jednego backend-db stacka.

3. Baza danych wynika z wybranego backend-db stacka

   Jest to świadome ograniczenie zakresu pracy. Użytkownik nie będzie mógł w podstawowej wersji dowolnie łączyć backendu z bazą danych. Jego decyzją będzie wybór jednego ze wspieranych backend-db stacków: FastAPI + SQLite albo drugiego stacka z PostgreSQL (ASP.NET Core albo Django). Dodanie większej liczby obsługiwanych stacków nie powinno wymagać zmiany założeń architektonicznych, ale zwiększyłoby ilość pracy implementacyjnej, testowej i dokumentacyjnej. Dlatego podstawowa wersja pracy zawiera tylko stacki wskazane w specyfikacji, z uwzględnieniem planowanej zmiany.

4. Kontrakty zamiast jakichkolwiek adapterów

   Ta zasada chroni wygenerowany projekt przed sztuczną warstwą abstrakcji, jaką byłby dowolny adapter. Nie chcę, żeby projekt miał dodatkowe adaptery tylko dlatego, że generator obsłuży inne kombinacje. Dzięki temu spójność i natywność wygenerowanego kodu zostanie osiągnięta przez kontrakty:
   - frontend jest kompatybilny z backendem, bo oba spełniają kontrakt API
   - backend-db stack jest zgodny z wymaganiami projektu, bo spełnia kontrakt danych

5. Natywność template packów

   Template pack będzie dostarczał kod, który jest naturalny dla danej technologii. Django nie zostanie wciśnięte w typową strukturę FastAPI, a Nuxt nie będzie udawać Reacta. Dlatego kluczowe będzie dokładne zapoznanie się ze wzorcami standardowymi dla obsługiwanych technologii, a następnie utworzenie każdego template packa zgodnie z nimi. Przykład konwencji:
   - Django -> Django ORM, migracje Django, struktura Django
   - FastAPI -> struktura FastAPI, osobna konfiguracja aplikacji, osobne modele/schemy
   - Nuxt -> routing oparty na plikach, struktura typowa dla Nuxta
   - React -> React Router, Vite, struktura typowa dla Reacta

   Jeśli wspólne będą jedynie wymagania, a nie struktura kodu, osiągniemy naturalny projekt, pozbawiony złych nawyków lub wymuszeń związanych z innymi frameworkami.

6. Wygenerowany projekt nie zależy runtime'owo od generatora

   Generator jest jedynie narzędziem do tworzenia projektu, a nie jego częścią. Projekt po przeniesieniu do katalogu docelowego ma funkcjonować bez generatora. Wygenerowany projekt nie powinien importować bibliotek generatora ani wymagać go do uruchamiania, testowania lub dalszego rozwijania.

7. Kontrolowane powtórzenia zamiast sztucznych abstrakcji

   W zwykłym projekcie często dąży się do DRY. W przypadku generatora zbyt agresywne DRY mogłoby jednak sprawić, że ucierpią na tym generowane projekty. Współdzielenie jednej abstrakcji między różnymi frameworkami skończyłoby się strukturą nienaturalną dla żadnego z nich. Z tego powodu akceptuję pewne powtórzenia, jeśli są konieczne, żeby:
   - template pack pozostał natywny
   - wygenerowany kod pozostał czytelny
   - framework działał zgodnie z typowymi dla siebie konwencjami
   - nowa technologia nie wymagała modyfikowania starej

   Dlatego wygenerowane projekty powinny być możliwie DRY, ale sam generator może świadomie zawierać kontrolowane powtórzenia w template packach.

## Ryzyka projektowe

- największe ryzyka projektu mają charakter architektoniczny, ponieważ błędne decyzje dotyczące kontraktów, template packów lub pipeline'u mogą utrudnić dalsze rozszerzanie generatora
- zbyt duża liczba kombinacji technologicznych może sprawić, że nie zdążę z pracą
- zbyt mała liczba kombinacji technologicznych może nie dać pewności, że dodawanie kolejnych nie wymaga modyfikacji istniejących
- jeśli drugim stackiem zostanie Django, podstawowy zakres obejmie wyłącznie backendy z ekosystemu Pythona. Wtedy projekt w ograniczonym stopniu zweryfikuje możliwość dodania backendu z innego języka programowania, np. Node.js, Java lub C#, mimo że z perspektywy architektonicznej powinno to być możliwe
- zbyt agresywne stosowanie zasady DRY może prowadzić do sztucznych abstrakcji między technologiami. W projekcie ważniejsze jest zachowanie natywności template packów oraz zgodność z zasadą open/closed, nawet kosztem kontrolowanego powtórzenia części kodu lub konfiguracji

## Architektura

### Przepływ i główne etapy działania

1. Pozyskanie danych wejściowych

   Generator zaczyna od otrzymania danych wejściowych. To jest jedynie deklaracja od użytkownika, co chce uzyskać:
   - nazwa projektu
   - katalog docelowy
   - frontend
   - backend-db stack
   - porty
   - zmienne środowiskowe

2. Normalizacja konfiguracji

   Generator przerabia dane wejściowe na spójną konfigurację wewnętrzną za pomocą wspólnego mechanizmu normalizacji danych wejściowych. Wartości zostają uporządkowane i uzupełnione wartościami domyślnymi, a brakujące sekrety zostają wylosowane. Powstaje z nich znormalizowana konfiguracja wewnętrzna, na której podstawie powstanie projekt. Dzięki temu zarówno kreator, jak i plik konfiguracyjny mogą być interpretowane tak samo.

3. Walidacja

   Generator waliduje konfigurację i sprawdza, czy jest ona obsługiwana. Sprawdza, czy porty nie mają konfliktów oraz czy da się utworzyć katalog docelowy. Jeśli katalog docelowy nie jest pusty, generator w trybie kreatora prosi o potwierdzenie, a w trybie pliku konfiguracyjnego wymaga flagi -f.

4. Stworzenie planu generacji

   Plan generacji jest zbiorem danych parametryzujących generację projektu. Zostanie on przekazany do pipeline'u. Na etapie planowania wykrywane są konflikty między packami, na przykład gdy dwa packi chcą wyrenderować ten sam plik. Plan odróżnia renderowanie całego pliku od składania go z contributions kilku packów i określa, jakie pliki składane zostaną stworzone.

5. Generowanie w stagingu

   Generator nie zaczyna od katalogu docelowego, tylko generuje projekt w stagingu, czyli tymczasowym katalogu roboczym. Na podstawie stałej listy kroków oraz planu generacji zostaje przeprowadzony cały proces - renderowanie template'ów, tworzenie struktury katalogów, zapis plików i przygotowanie konteneryzacji.

6. Weryfikacja

   Etap sprawdzenia, czy wygenerowany projekt rzeczywiście spełnia wymagania. Jest to główne odróżnienie tego generatora od prostego kopiowania template'ów. Poprawność projektu nie jest oceniana tym, że pliki powstały, tylko tym, że przechodzą wymagane testy.
   Weryfikacja sprawdza, czy Docker Compose uruchamia wymagane kontenery, backend odpowiada na `GET /health/ready`, backend komunikuje się z bazą, frontend komunikuje się z backendem, wszystkie testy przechodzą oraz czy działa happy path rejestracji, logowania i pobrania danych aktualnego użytkownika. Test happy path jest częścią wygenerowanego projektu, więc użytkownik może go później uruchomić samodzielnie.

7. Finalizacja

   Ostatni etap, przenoszący zweryfikowany projekt do katalogu docelowego. Jeśli weryfikacja nie zakończy się sukcesem, projekt nie zostaje przeniesiony do katalogu docelowego.

### Podział systemu na główne części

1. Core

Core jest głównym modułem sterującym generatora. Core nie może znać szczegółów frameworków, z jakich korzysta. Musi on orkiestrować cały proces generacji:

- uruchomienie CLI
- wczytanie danych
- normalizacja konfiguracji
- walidacja konfiguracji
- Planning
- zarządzanie wykonaniem kroków pipeline'u
- zapis i odczyt stanu generacji (opcjonalnie)
- obsługa błędów
- przekazanie wyniku do outputu
- zebranie statystyk

Dzięki temu, w przypadku rozszerzania o kolejne technologie, core nie powinien wymagać istotnych modyfikacji.

2. Pipeline

Zarządzany przez core iterowalny proces, przechodzący przez renderowanie, weryfikację i output. Pipeline umożliwia przechodzenie ze stanu do stanu w przód, a informacje o artefaktach i efektach ubocznych kroków pozwalają core'owi wykonać cleanup albo, opcjonalnie, wznowienie procesu.

3. Template packs

Część systemu, która dostarcza kod i konfigurację dla konkretnych technologii. Template packi znają szczegóły frameworków, mieści się w nich docelowa struktura generowanego kodu.
Template packi powinny być możliwie niezależne od siebie i komunikować się przez kontrakty oraz contributions. Jeśli autor chce rozszerzyć generator o obsługę kolejnej technologii, po prostu dodaje kolejny template pack. To tam mieści się cały kod, konfiguracja, obsługa kontraktów. Dzięki temu wystarczy w zasadzie dobrze znać wybrany framework, żeby móc utworzyć dla niego template pack.
Template packi dzielą się na dwa rodzaje: frontend i backend-db. Każdy template pack zawiera template'y całościowe, z których powstają całe pliki, oraz template'y częściowe (contributions), z których składany jest wspólny plik. Na przykład `docker-compose.yml`, `.env` i `README.md` w katalogu głównym projektu powstają z contributions kilku packów.

4. Planning

Część odpowiedzialna za przetłumaczenie konfiguracji na plan generacji. Na tym etapie konfiguracja zostaje zamieniona na zestaw template packów, contributions i danych potrzebnych do renderowania. Dzięki niemu proces jest przewidywalny i deterministyczny oraz gwarantuje poprawny plan.

5. Rendering

Proces zmieniający template'y wybrane w planie generacji na realne pliki w katalogu. Renderer przyjmuje template packi i renderuje pliki całościowe oraz pliki składane z contributions.

6. Output

Output odpowiada za fizyczny zapis wyniku, zarówno do stagingu, jak i do katalogu docelowego. Pilnuje też, żeby wynikowa struktura nie była uszkodzona.

Zadania outputu:

- zapewnienie pustego stagingu
- zapis plików
- przeniesienie projektu do katalogu docelowego
- czyszczenie po błędzie zgodnie z decyzją podjętą przez core
- ochrona katalogu docelowego przed uszkodzonym wynikiem

7. State (opcjonalny)

Zapisany stan działania generatora. Ten komponent jest opcjonalny i powstanie, jeśli wystarczy czasu. Bezpieczne korzystanie ze stanów jest możliwe, ponieważ zakładamy, że wynik dla każdej konfiguracji jest deterministyczny. Dzięki temu core może łatwo wstrzymać i przywrócić proces, obsłużyć błąd w jednym z kroków i powtórzyć krok bez konieczności powtarzania całego procesu generacji oraz łatwo wyczyścić stan i rozpocząć od nowa. Stan pozwala wykryć, czy konfiguracja została zmieniona. Jeśli hash konfiguracji nie zgadza się ze stanem zapisanym z poprzedniego przebiegu, core nie wznawia działania, tylko czyści stan i rozpoczyna proces od nowa.

8. Verification

Weryfikacja sprawdza, czy projekt w stagingu działa poprawnie. Wygenerowany projekt, zanim trafi do katalogu docelowego, jest dokładnie sprawdzany w stagingu. Dzięki temu nie wprowadzamy niedziałającego projektu do katalogu docelowego. Weryfikacja jest wykonywana jako jeden lub kilka kroków pipeline'u zarządzanego przez core.

9. Statistics

Część odpowiedzialna za mierzenie i raportowanie przebiegu generacji. Statystyki zbierają:

- czas całej generacji
- czas poszczególnych etapów
- wybraną kombinację technologiczną
- liczbę wygenerowanych plików
- liczbę użytych template packów
- status verification
- informację o błędzie, jeśli wystąpił

Mogą też służyć do porównywania czasu trwania etapów oraz czasu generacji różnych kombinacji technologicznych.

## Dotychczasowe wyniki pracy (5min)

### Dokumentacja

Zatwierdzona przez promotora:

- dokumentacja wstępna (117 linii)
- specyfikacja (522 linie)
- kryteria akceptacyjne (586 linii, 65 kryteriów)
- architektura (1004 linie)

### Template packi

- działający backend FastAPI + SQLite (API, Docker, README) z narzędziami jakości (ruff, mypy, pytest, `make check`)
- w toku: testy backend-db, test dymny i contributions
- manifest template packa Nuxt

### Generator

- infrastruktura generatora: struktura repozytorium, logger, narzędzia jakości (ruff, mypy, pytest, vulture, deptry, bandit, pip-audit, prettier) spięte w `make check`
- ustrukturyzowanie i zaplanowanie całej pracy
- schematy pliku konfiguracyjnego i manifestu template packa
- wczytywanie manifestów i dopasowywanie template packów do konfiguracji
- wczytywanie i normalizacja konfiguracji gotowe, walidacja w toku
- szkielet core z całym przepływem etapów, w którym CLI, walidacja i pipeline są na razie atrapami

## Plan prac na ten semestr i program minimum (2min)

### Faza 1

- domknięcie template packa FastAPI: testy, contributions, poprawki

### Faza 2

- implementacja core: CLI, wykonanie planu generacji, obsługa pipeline'u
- implementacja kroków pipeline'u
- określenie formatu planu generacji, implementacja
- implementacja renderera i outputu, procedura weryfikacji i finalizacji

### Faza 3

- template pack Nuxta

### Faza 4

- dokończenie generatora

### Faza 5

- napisanie pracy inżynierskiej w docelowym formacie

### Faza 6

- okrojony template pack React oraz drugi backend-db stack (ASP.NET Core albo Django)

## Slajd końcowy

- powtórzenie slajdu tytułowego
