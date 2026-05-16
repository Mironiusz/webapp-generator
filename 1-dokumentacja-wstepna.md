# Generator szablonów aplikacji webowych (webapp boilerplate generator)

## Opis problemu

Wielu programistów doskonale potrafi rozszerzać i edytować aplikację webową. Gorzej, kiedy trzeba postawić nową - nikt tego nie lubi, a mało kto potrafi bez przypomnienia sobie w dokumentacji poprawnie uruchomić Vite, napisać podstawowy routing, zainstalować odpowiednie pakiety, połączyć frontend z backendem bez problemów z CORS i stworzyć Dockerfile, który od razu zadziała. Do tego, nieważne jak dobry programista by nie był, to wszystko po prostu zabiera czas.
Dlatego właśnie postanowiłem stworzyć generator aplikacji webowych, który wszystkie te nieprzyjemne boilerplate'owe kroki wykona za użytkownika.

## Cel projektu

Celem projektu jest zaprojektowanie i implementacja narzędzia CLI generującego konteneryzowane szkielety aplikacji webowych na podstawie kreatora lub pliku konfiguracyjnego. Generator ma ograniczyć ilość powtarzalnej pracy potrzebnej do uruchomienia nowej aplikacji oraz zapewnić spójny, testowalny i rozszerzalny punkt startowy dla dalszego rozwoju projektu.

## Efekt dla użytkownika

Po przejściu przez kreator aplikacji lub uruchomieniu generatora z plikiem konfiguracyjnym powstaje działający, konteneryzowany szkielet aplikacji webowej z konfiguracją środowiskową, który wystarczy rozszerzać i modyfikować.

## Opis działania

- użytkownik uruchamia kreator albo wskazuje plik konfiguracyjny
- wybiera lub deklaruje frontend (Vue, React)
- wybiera lub deklaruje backend (Django, FastAPI)
- baza danych w podstawowym zakresie projektu nie jest osobnym wyborem użytkownika. Generator wykorzystuje PostgreSQL jako stały element infrastruktury.

Następnie generator tworzy projekt zawierający:

### Funkcjonalność bazowa

- moduły komunikują się ze sobą
- na frontendzie działa routing, strona logowania oraz strona app
- backend wystawia spójny kontrakt HTTP API niezależnie od wybranego frameworka, obejmujący health, login (prosty JWT) i CORS
- backend-db stack dostarcza minimalny model użytkownika, migracje oraz dane wymagane do działania logowania
- powstają bazowe testy integracyjne dla połączenia frontend-backend i backend-db
- powstają bazowe testy jednostkowe dla backendu

### Funkcjonalność produkcyjna

- powstaje .env i .env.example
- powstaje docker-compose.yml i odpowiednie pliki Dockerfile
- powstaje .gitignore i .dockerignore
- powstaje instrukcja README.md opisująca architekturę wygenerowanego projektu oraz sposób jego rozszerzania i edycji

### Funkcjonalność techniczna

- idempotentny pipeline (pipeline zapisuje stan kroków, w razie błędu można wznowić działanie od ostatniego kroku zakończonego sukcesem, wyniki kroku są zapisywane do docelowego folderu dopiero po jego poprawnym zakończeniu)
- walidacja kompatybilności (konflikty portów, zmienne środowiskowe podane przez użytkownika, zależności)
- tryb kreatora albo pliku konfiguracyjnego
- mierzenie czasu generacji i podanie statystyk

### Potencjalne rozszerzenia

- generacja produkcyjnego modułu do logów na serwerze
- formatter i linter
- ...

## Architektura

Architektura opisana jest w dokumencie 4-architektura.md

## Wspierane kombinacje technologiczne

W podstawowym zakresie projektu wspierane są następujące kombinacje:

- Vue + FastAPI + PostgreSQL
- React + FastAPI + PostgreSQL
- Vue + Django + PostgreSQL
- React + Django + PostgreSQL

## Kluczowe decyzje projektowe

- mówiąc o "wersji produkcyjnej", odnoszę się do kompletnego, rozszerzalnego i uruchamialnego szkieletu aplikacji z podstawową konfiguracją bezpieczeństwa aplikacyjnego, konfiguracją środowiskową, konteneryzacją oraz testami, ale bez infrastruktury serwerowej
- frontend jest niezależny od backendu i komunikuje się wyłącznie przez kontrakt HTTP API
- backend i baza danych są traktowane jako sprzężony backend-db stack
- PostgreSQL jest jedyną wspieraną bazą danych w podstawowym zakresie projektu
- każdy backend może posiadać własną natywną schemę i migracje
- wspólna część danych jest definiowana jako minimalny kontrakt danych. Kontrakt danych nie musi oznaczać identycznej fizycznej struktury tabel w każdym backendzie, ale określa minimalne wymagania funkcjonalne i strukturalne potrzebne do działania aplikacji
- elementy specyficzne dla frameworka są traktowane jako rozszerzenia backend-db stacka
- generator nie dodaje runtime'owej zależności do wygenerowanego projektu

Projekt opiera się na dwóch głównych kontraktach:

- kontrakcie HTTP API, który uniezależnia frontend od backendu
- kontrakcie danych, który określa minimalne wymagania wobec backend-db stacka

Dzięki temu dodawanie kolejnych wspieranych frameworków powinno polegać głównie na dodaniu nowego template packa spełniającego istniejące kontrakty, bez konieczności modyfikowania pozostałych kombinacji technologicznych.

## Zakres poza projektem

Projekt nie obejmuje:

- Kubernetes
- TLS
- SSO
- Nginx
- load balancingu
- reverse proxy
- automatycznego CI/CD
- podziału na osobne kontenery dev i prod
- innych typowo serwerowych funkcjonalności

## Ryzyka projektowe

- największe ryzyka projektu mają charakter architektoniczny, ponieważ błędne decyzje dotyczące kontraktów, template packów lub pipeline'u mogą utrudnić dalsze rozszerzanie generatora
- zbyt duża liczba kombinacji technologicznych może zwiększyć koszt testowania
- zbyt mała liczba kombinacji technologicznych może nie dać pewności, że dodawanie kolejnych nie wymaga modyfikacji istniejących
- backendy różnią się podejściem do auth, ORM i migracji. Z tego powodu kontrakt między backendem a warstwą danych musi być bardzo dobrze przemyślany i możliwy do rozszerzenia o kolejne frameworki backendowe
- ponieważ podstawowy zakres obejmuje wyłącznie backendy z ekosystemu Pythona, projekt w ograniczonym stopniu weryfikuje i testuje możliwość dodania backendu z innego języka programowania, np. Node.js, Java lub Go, mimo że z perspektywy architektonicznej powinno to być możliwe
- zbyt agresywne stosowanie zasady DRY może prowadzić do sztucznych abstrakcji między technologiami. W projekcie ważniejsze jest zachowanie natywności template packów oraz zgodność z zasadą open/closed, nawet kosztem kontrolowanego powtórzenia części kodu lub konfiguracji

## Weryfikacja

Poprawność zostanie zweryfikowana przez wygenerowanie projektu, a następnie uruchomienie docker-compose.yml i sprawdzenie poprawności testów oraz działania. Celem jest, aby proces generacji sterowany był plikiem konfiguracyjnym lub kreatorem. Zadziałać powinna każda wspierana kombinacja.

Za sukces uznaję wygenerowanie projektu, który uruchamia się bez dodatkowej konfiguracji oraz przechodzi zestaw testów automatycznych dla wybranej konfiguracji i jest możliwy do uruchomienia przez użytkownika.

Dokładne kryteria akceptacyjne opisane są w dokumencie 3-kryteria-akceptacyjne.md
