Generator szablonów aplikacji webowych (webapp boilerplate generator)
Założenie:
Wielu programistów doskonale potrafi rozszerzać i edytować aplikację webową. Gorzej, kiedy trzeba postawić nową - nikt tego nie lubi, a mało kto potrafi bez przypomnienia sobie w dokumentacji poprawnie uruchomić vite, napisać podstawowy routing, zainstalować odpowiednie pakiety, połączyć frontend z backendem bez problemów z CORS i stworzyć dockerfile, który od razu zadziała. Do tego, nieważne jak dobry programista by nie był, to wszystko po prostu zabiera czas.
Dlatego właśnie postanowiłem stworzyć generator aplikacji webowych, który wszystkie te nieprzyjemne boilerplate'owe kroki wykona za użytkownika.

Efekt dla użytkownika:
Po przejściu przez kreator aplikacji, powstaje działający szkielet aplikacji webowej w wersji produkcyjnej (uruchamialny zestaw kontenerów z konfiguracją środowiskową), który wystarczy rozszerzać i modyfikować.

Opis działania:

- użytkownik uruchamia kreator
- wybiera frontend (vue, react)
- wybiera backend (django, fastapi)
- wybiera db (sqlite, postgres)
  Ewentualnie, w przypadku trudności z implementacją tak dużej ilości kombinacji, dopuszczam ograniczenie wspieranych kombinacji do fastapi + sqlite oraz django + postgres.

Następnie generator tworzy projekt zawierający:
Funkcjonalność bazowa:

- moduły komunikują się ze sobą
- na frontendzie działa routing, strona logowania oraz strona app
- na backendzie działa health, login (prosty JWT) i CORS
- w bazie danych jest tabela User i działają migracje
- powstają bazowe testy integracyjne dla połączenia frontend-backend i backend-db
- powstają bazowe testy jednostkowe dla backendu

Funkcjonalność produkcyjna:

- powstaje .env
- powstaje docker-compose i odpowiednie dockerfile
- powstaje gitignore
- powstaje instrukcja readme, jaka jest architektura, jak rozszerzać i edytować

Funkcjonalność techniczna:

- idempotentny pipeline (pipeline zapisuje stan kroków, w razie błędu można wznowić działanie od ostatniego kroku zakończonego sukcesem, wyniki kroku są zapisywane do docelowego folderu dopiero po jego poprawnym zakończeniu)
- walidacja kompatybilności (konflikty portów, zmienne środowiskowe podane przez użytkownika, zależności)
- tryb kreatora albo pliku konfiguracyjnego
- mierzenie czasu generacji i podanie statystyk

Potencjalne rozszerzenia:

- automatyczny push do repozytorium
- generacja produkcyjnego modułu do logów na serwerze
- formatter i linter
- ...

Wstępna architektura:

- Core: orchestrator pipeline'u, model configu, walidacja, logowanie postępu
- Templates: źródła szablonów
- Generators: moduły generujące kod i konfigurację na podstawie szablonów i configu. Wykorzystywane przez core.
- Post-processing: wszystkie niecore'owe funkcjonalności, wywoływane na już wygenerowanym kodzie
- Output: zapis do ostatecznego katalogu, opcjonalny push

- deterministyczne wyjście dla danej konfiguracji, idempotentność
- instalowalność przez pip

Zakres nie obejmuje:

- kubernetes
- tls
- sso
- nginx, load balancing, reverse proxy
- inne typowo serwerowe funkcjonalności.

Weryfikacja:
Poprawność zostanie zweryfikowana przez wygenerowanie projektu, a następnie uruchomienie docker-compose i sprawdzenie poprawności testów oraz działania. Celem jest, aby proces generacji sterowany był wyłącznie plikiem konfiguracyjnym. Zadziałać powinna każda wspierana kombinacja.

Za sukces uznaję wygenerowanie projektu, który uruchamia się bez dodatkowej konfiguracji oraz przechodzi zestaw testów automatycznych dla wybranej konfiguracji i jest możliwy do uruchomienia przez użytkownika.
