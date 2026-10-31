# Generator szkieletów aplikacji webowych (webapp boilerplate generator)

Stan: 31.10.2026

## Opis problemu

Wielu programistów doskonale potrafi rozszerzać i edytować aplikację webową. Gorzej, kiedy trzeba postawić nową - nikt tego nie lubi, a mało kto potrafi bez przypomnienia sobie w dokumentacji poprawnie uruchomić Vite, napisać podstawowy routing, zainstalować odpowiednie pakiety, połączyć frontend z backendem bez problemów z CORS i stworzyć Dockerfile, który od razu zadziała. Do tego, nieważne jak dobry programista by nie był, to wszystko po prostu zabiera czas.
Dlatego właśnie postanowiłem stworzyć generator szkieletów aplikacji webowych, który wszystkie te nieprzyjemne boilerplate'owe kroki wykona za użytkownika.

## Cel projektu

Celem projektu jest zaprojektowanie i implementacja narzędzia CLI generującego konteneryzowane szkielety aplikacji webowych na podstawie kreatora lub pliku konfiguracyjnego. Generator ma ograniczyć ilość powtarzalnej pracy potrzebnej do uruchomienia nowej aplikacji oraz zapewnić spójny, testowalny i rozszerzalny punkt startowy dla dalszego rozwoju projektu.

## Efekt dla użytkownika

Po przejściu przez kreator aplikacji lub uruchomieniu generatora z plikiem konfiguracyjnym powstaje działający, konteneryzowany szkielet aplikacji webowej z konfiguracją środowiskową, który wystarczy rozszerzać i modyfikować.

## Opis działania

- użytkownik uruchamia kreator albo wskazuje plik konfiguracyjny
- wybiera lub deklaruje frontend (Nuxt)
- wybiera lub deklaruje backend-db stack (FastAPI + SQLite, Django + PostgreSQL)

Następnie generator tworzy projekt zawierający:

### Funkcjonalność bazowa

- części projektu komunikują się ze sobą
- na frontendzie działa routing, strona logowania i rejestracji oraz strona aplikacji
- backend wystawia spójny kontrakt HTTP API niezależnie od wybranego frameworka, obejmujący endpointy health, rejestrację, logowanie tokenem JWT, pobranie danych aktualnego użytkownika i CORS
- backend-db stack dostarcza minimalny model użytkownika, migracje oraz dane wymagane do działania podstawowego mechanizmu uwierzytelniania
- powstają bazowe testy jednostkowe backendu i frontendu, testy integracyjne frontend-backend i backend-db oraz test happy path

### Funkcjonalność produkcyjna

- powstają pliki .env i .env.example w katalogu głównym i w każdej części projektu
- powstaje docker-compose.yml i odpowiednie pliki Dockerfile
- powstaje .gitignore i .dockerignore
- powstaje instrukcja README.md opisująca architekturę wygenerowanego projektu oraz sposób jego rozszerzania i edycji

### Funkcjonalność techniczna

- idempotentny pipeline (każde uruchomienie zaczyna od zera w katalogu roboczym, projekt trafia do katalogu docelowego dopiero po pozytywnej weryfikacji, a po błędzie generator sprząta cały run)
- walidacja konfiguracji (konflikty portów, katalogi, zmienne środowiskowe podane przez użytkownika)
- tryb kreatora albo pliku konfiguracyjnego
- mierzenie czasu generacji i podanie statystyk

### Potencjalne rozszerzenia

- generacja produkcyjnego modułu do logów na serwerze
- Nginx
- backend-db stack używający ASP.NET Core + PostgreSQL
- frontend w React
- ...

## Architektura

Architektura opisana jest w dokumencie 4-architektura.md

## Wspierane kombinacje technologiczne

W podstawowym zakresie projektu wspierane są następujące kombinacje:

- Nuxt + FastAPI + SQLite
- Nuxt + Django + PostgreSQL

## Kluczowe decyzje projektowe

- mówiąc o "wersji produkcyjnej", odnoszę się do kompletnego, rozszerzalnego i uruchamialnego szkieletu aplikacji z podstawową konfiguracją bezpieczeństwa aplikacyjnego, konfiguracją środowiskową, konteneryzacją oraz testami, ale bez infrastruktury serwerowej
- frontend jest niezależny od backendu i komunikuje się wyłącznie przez kontrakt HTTP API
- backend i baza danych są traktowane jako sprzężony backend-db stack
- każdy backend może posiadać własną natywną schemę i migracje
- wspólna część danych jest definiowana jako minimalny kontrakt danych. Kontrakt danych nie musi oznaczać identycznej fizycznej struktury tabel w każdym backendzie, ale określa minimalne wymagania funkcjonalne i strukturalne potrzebne do działania aplikacji
- backend może mieć dodatkowe tabele techniczne wymagane przez framework, o ile nie narusza to kontraktu danych
- generator nie dodaje runtime'owej zależności do wygenerowanego projektu
- mechanizm uwierzytelniania w podstawowej wersji obejmuje rejestrację, logowanie oraz JWT. Projekt nie implementuje pełnego systemu zarządzania tożsamością użytkowników, dlatego reset hasła, SSO, MFA, potwierdzanie adresu email i integracja z dostawcą poczty pozostają poza podstawowym zakresem projektu

Projekt opiera się na dwóch głównych kontraktach:

- kontrakcie HTTP API, który uniezależnia frontend od backendu
- kontrakcie danych, który określa minimalne wymagania wobec backend-db stacka

Dzięki temu dodawanie kolejnych wspieranych frameworków powinno polegać głównie na dodaniu nowego template packa spełniającego istniejące kontrakty, bez konieczności modyfikowania pozostałych kombinacji technologicznych.

## Zakres poza projektem

Projekt w podstawowej wersji nie obejmuje elementów wymienionych w ograniczeniach specyfikacji (15), m.in. Kubernetes, TLS, SSO, CI/CD i resetu hasła.

## Ryzyka projektowe

- największe ryzyka projektu mają charakter architektoniczny, ponieważ błędne decyzje dotyczące kontraktów, template packów lub pipeline'u mogą utrudnić dalsze rozszerzanie generatora
- zbyt duża liczba kombinacji technologicznych może zwiększyć koszt testowania
- zbyt mała liczba kombinacji technologicznych może nie dać pewności, że dodawanie kolejnych nie wymaga modyfikacji istniejących
- backendy różnią się podejściem do auth, ORM i migracji. Z tego powodu kontrakt danych musi być bardzo dobrze przemyślany i możliwy do rozszerzenia o kolejne frameworki backendowe
- ponieważ podstawowy zakres obejmuje wyłącznie backendy z ekosystemu Pythona, projekt w ograniczonym stopniu weryfikuje i testuje możliwość dodania backendu z innego języka programowania, np. Node.js, Java lub C#, mimo że z perspektywy architektonicznej powinno to być możliwe
- zbyt agresywne stosowanie zasady DRY może prowadzić do sztucznych abstrakcji między technologiami. W projekcie ważniejsze jest zachowanie natywności template packów oraz zgodność z zasadą open/closed, nawet kosztem kontrolowanego powtórzenia części kodu lub konfiguracji

## Weryfikacja

Poprawność zostanie zweryfikowana przez wygenerowanie projektu, a następnie uruchomienie docker-compose.yml i sprawdzenie poprawności testów oraz działania. Celem jest, aby proces generacji sterowany był plikiem konfiguracyjnym lub kreatorem. Zadziałać powinna każda wspierana kombinacja.

Za sukces uznaję wygenerowanie projektu, który uruchamia się bez dodatkowej konfiguracji oraz przechodzi zestaw testów automatycznych dla wybranej konfiguracji i jest możliwy do uruchomienia przez użytkownika.

Dokładne kryteria akceptacyjne opisane są w dokumencie 3-kryteria-akceptacyjne.md
