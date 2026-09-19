# Specyfikacja

Stan: 28.05.2026

## 1. Cel dokumentu

Dokument określa, co generator ma robić oraz jakie warunki musi spełniać wygenerowany projekt, ale nie narzuca sposobu implementacji wewnętrznej generatora.

## 2. Zakres specyfikacji

Specyfikacja obejmuje:

- działanie generatora
- format danych wejściowych
- wymagany wynik generacji
- minimalne wymagania wobec wygenerowanej aplikacji
- kontrakt API
- kontrakt danych
- testy
- wymagania niefunkcjonalne

Specyfikacja nie obejmuje:

- konkretnych klas i modułów generatora
- struktury wewnętrznej implementacji
- szczegółów architektury template packów

## 3. Role użytkowników

- Użytkownik generatora - programista, który chce utworzyć początkowy szkielet aplikacji webowej.
- Autor rozszerzenia - programista dodający obsługę nowej technologii

## 4. Tryby pracy generatora

Generator zapewni dwa tryby: kreatora i pliku konfiguracyjnego. Wynika to z założenia, że tryb kreatora jest przystępny, ale po kilku razach przechodzenie przez niego w podobny sposób staje się irytujące. Ten problem rozwiązuje plik konfiguracyjny. Umożliwi on też szybsze testowanie generatora.

### 4.1 Tryb kreatora

Użytkownik odpowiada na pytania i podejmuje decyzje:

- nazwa projektu
- ścieżka docelowa
- frontend
- backend-db stack
- porty albo wartości domyślne
- dane środowiskowe albo wartości domyślne

### 4.2 Tryb pliku konfiguracyjnego

Generator przyjmuje plik konfiguracyjny i działa bez jakiejkolwiek interakcji.

## 5. Dane wejściowe generatora

Dane wejściowe są określane na podstawie kreatora lub pliku konfiguracyjnego.

- project.name
- project.output_dir
- frontend.framework
- backend.framework
- database.engine
- ports.frontend
- ports.backend
- ports.database (gdy backend korzysta z osobnej bazy danych)
- env

## 6. Wspierane technologie i kombinacje

Generator musi wspierać następujące kombinacje:

- Vue + FastAPI + SQLite
- React + FastAPI + SQLite
- Vue + Django + PostgreSQL
- React + Django + PostgreSQL

Generator w tej wersji nie musi obsługiwać kombinacji spoza tej listy, ale musi być rozszerzalny o nowe frameworki frontendowe i backendowe.

## 7. Wynik działania generatora

Generowane są:

- katalog projektu
- frontend
- backend
- konfiguracja Docker Compose
- konfiguracja środowiskowa
- pliki ignorowania
- dokumentacja README
- testy

### 7.1 Struktura wygenerowanego projektu

|--/docs
|--/frontend
|--/backend
|--/database \*opcjonalny
|--.env
|--.env.example
|--README.md
|--docker-compose.yml
|--.gitignore
|--.dockerignore

## 8. Wymagania funkcjonalne generatora

- Generator musi umożliwiać utworzenie projektu na podstawie kreatora.
- Generator musi umożliwiać utworzenie projektu na podstawie pliku konfiguracyjnego.
- Generator musi walidować konfigurację przed rozpoczęciem generacji.
- Generator musi wykrywać niewspierane kombinacje technologiczne.
- Generator musi wykrywać konflikty portów.
- Generator musi utworzyć projekt w katalogu docelowym.
- Generator musi umożliwiać wznowienie generacji po błędzie.
- Generator musi raportować czas generacji i podstawowe statystyki.

Generator musi przerwać działanie przed rozpoczęciem generacji, jeśli:

- wybrano niewspieraną kombinację technologii
- brakuje wymaganych danych wejściowych
- wskazana ścieżka outputu jest niepoprawna
- porty wymagane przez usługi są skonfliktowane
- wartości środowiskowe są niepoprawne

## 9. Wymagania funkcjonalne wygenerowanej aplikacji

### 9.1 Frontend

- routing
- strona logowania
- strona rejestracji
- strona aplikacji
- strona 404
- klient HTTP do backendu
- obsługa tokena JWT
- obsługa błędu logowania
- testy jednostkowe
- testy integracyjne

### 9.2 Backend

- endpoint health, db i ready
- endpoint login
- endpoint register
- endpoint zwracający dane aktualnego użytkownika
- obsługa CORS
- obsługa JWT
- testy jednostkowe
- testy integracyjne

### 9.3 Baza danych

Baza danych jest w PostgreSQL lub w SQLite.

Backend zapewnia:

- migracje
- minimalny model użytkownika
- strukturę danych wymaganą do działania podstawowego mechanizmu uwierzytelniania

### 9.4 Komunikacja

- działa komunikacja frontend-backend
- działa komunikacja backend-db

"Działanie" definiuję przejściem testów integracyjnych.

## 10. Kontrakt HTTP API

### 10.1 Zasady wspólne

Endpointy health są wystawione bez prefixu. Pozostałe endpointy są wystawione pod prefixem `/api/v1`. Ścieżki w kontrakcie są podane w pełnej formie.

Każde body requestu i każda odpowiedź mają typ `application/json`.

#### Format błędów

Każdy błąd ma postać:

```json
{
	"detail": "Komunikat błędu"
}
```

Wartości `detail` są stałymi wymienionymi przy endpointach, żeby testy mogły porównywać je dosłownie.

Każdy endpoint może dodatkowo zwrócić status 500 z `detail` o wartości `Internal server error` dla nieobsłużonego błędu serwera. Kryteria akceptacyjne nie testują tej odpowiedzi.

#### Walidacja danych wejściowych

Naruszenie którejkolwiek reguły daje status 400 z `detail` o wartości `Invalid request data`. Odpowiedź nie wskazuje, która reguła została naruszona, dlatego frontend stosuje te same reguły po swojej stronie.

- brak wymaganego pola albo zły typ pola
- `email`: poprawny adres email, najwyżej 254 znaki
- `password`: od 8 do 128 znaków
- `username`: jeśli podany, od 3 do 64 znaków

#### Obiekt użytkownika

Wszystkie endpointy zwracające użytkownika używają tego samego kształtu:

```json
{
	"id": 1,
	"username": "admin",
	"email": "admin@example.com",
	"is_active": true
}
```

Pole `username` ma wartość `null`, gdy użytkownik nie podał go przy rejestracji. Hash hasła nigdy nie jest zwracany.

### 10.2 GET /health

Endpoint służy do sprawdzenia, czy backend odpowiada. Nie sprawdza bazy danych.

#### Response 200

```json
{
	"status": "ok"
}
```

### 10.3 GET /health/db

Endpoint służy do sprawdzenia, czy backend łączy się z bazą danych.

Pole `database_status` przyjmuje wartości `up` albo `down`.

#### Response 200

```json
{
	"status": "ok",
	"database_status": "up"
}
```

#### Response 503

```json
{
	"status": "degraded",
	"database_status": "down"
}
```

### 10.4 GET /health/ready

Endpoint służy do sprawdzenia, czy backend jest gotowy do obsługi ruchu: baza danych odpowiada i ma wdrożone wszystkie migracje.

Pole `schema_status` przyjmuje wartości:

- `ready`: schema jest zgodna z najnowszą migracją
- `not_migrated`: baza odpowiada, ale brakuje migracji
- `unknown`: nie dało się sprawdzić schemy, bo baza nie odpowiada

#### Response 200

```json
{
	"status": "ok",
	"database_status": "up",
	"schema_status": "ready"
}
```

#### Response 503, brak migracji

```json
{
	"status": "degraded",
	"database_status": "up",
	"schema_status": "not_migrated"
}
```

#### Response 503, baza nie odpowiada

```json
{
	"status": "degraded",
	"database_status": "down",
	"schema_status": "unknown"
}
```

### 10.5 POST /api/v1/auth/register

Endpoint służy do utworzenia konta użytkownika. Pole `username` jest opcjonalne.

#### Request

```json
{
	"username": "admin",
	"email": "admin@example.com",
	"password": "password"
}
```

#### Response 201

```json
{
	"id": 1,
	"username": "admin",
	"email": "admin@example.com",
	"is_active": true
}
```

#### Response 400

```json
{
	"detail": "Invalid request data"
}
```

#### Response 409

Zwracany, gdy istnieje już użytkownik z takim samym `email` albo takim samym `username`. Odpowiedź nie wskazuje, które pole koliduje.

```json
{
	"detail": "User already exists"
}
```

### 10.6 POST /api/v1/auth/login

Endpoint służy do zalogowania użytkownika i zwrócenia tokena JWT.

#### Request

```json
{
	"email": "admin@example.com",
	"password": "password"
}
```

#### Response 200

```json
{
	"access_token": "<jwt>",
	"token_type": "bearer"
}
```

#### Response 400

```json
{
	"detail": "Invalid request data"
}
```

#### Response 401

Zwracany dla nieistniejącego adresu email i dla złego hasła. Odpowiedź nie rozróżnia tych przypadków.

```json
{
	"detail": "Invalid credentials"
}
```

#### Response 403

Zwracany, gdy dane logowania są poprawne, ale użytkownik jest nieaktywny. Nieaktywny użytkownik nie dostaje tokena.

```json
{
	"detail": "Inactive user"
}
```

### 10.7 GET /api/v1/auth/me

Endpoint służy do pobrania danych aktualnie zalogowanego użytkownika na podstawie tokena JWT.

#### Request

Brak body.

Wymagany nagłówek:

```text
Authorization: Bearer <access_token>
```

#### Response 200

```json
{
	"id": 1,
	"username": "admin",
	"email": "admin@example.com",
	"is_active": true
}
```

#### Response 401

Zwracany, gdy nagłówka brakuje, token jest niepoprawny albo wygasł.

```json
{
	"detail": "Not authenticated"
}
```

#### Response 403

```json
{
	"detail": "Inactive user"
}
```

## 11. Kontrakt danych

Minimalny model użytkownika musi pozwalać na:

- jednoznaczną identyfikację użytkownika
- logowanie za pomocą emaila
- rejestrację za pomocą emaila
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

Kontrakt danych nie wymaga identycznej fizycznej struktury wszystkich tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez framework.

## 12. Wymagania środowiskowe

Środowiskiem wygenerowanego projektu będzie zbiór kontenerów Docker. Projekt uruchamiany jest przez:

```
docker compose up -d --build
```

Każda konfiguracja zawiera kontenery:

- backend
- frontend

Dodatkowy kontener database powstaje dla stacków korzystających z osobnej usługi bazy danych, np. Django + PostgreSQL. W przypadku SQLite baza danych działa jako plik obsługiwany przez backend.

Wymagane pliki poza kontenerami:

- .env
- .env.example
- docker-compose.yml
- Dockerfile frontendowy
- Dockerfile backendowy

## 13. Wymagania testowe

- testy jednostkowe backendu
- testy jednostkowe frontendu
- testy integracyjne backend-db
- testy integracyjne frontend-backend
- test uruchomieniowy potwierdzający, że wygenerowany projekt startuje przez docker compose

## 14. Wymagania niefunkcjonalne

### Idempotentność

Ponowne uruchomienie generatora dla tej samej konfiguracji nie może prowadzić do niespójnego lub częściowo uszkodzonego projektu.

### Deterministyczność

Dla tej samej konfiguracji generator powinien tworzyć taki sam wynik strukturalny.

### Rozszerzalność

Dodanie nowego frontendu albo backendu nie powinno wymagać modyfikacji istniejących wspieranych kombinacji technologicznych.

### Niezależność wygenerowanego projektu od generatora

Wygenerowany projekt musi być możliwy do uruchomienia bez generatora.

### Jakość wygenerowanego projektu

Wygenerowany projekt musi spełniać szeroko pojęte dobre praktyki programistyczne, między innymi:

- zasady SOLID
- zasada DRY
- testy jednostkowe dla kluczowych elementów backendu i frontendu
- testy integracyjne potwierdzające działającą komunikację frontend-backend oraz backend-db
- samodokumentujący się, czytelny kod z docstringami funkcji, ale bez komentarzy linijkowych
- pliki dokumentacyjne informujące, jak rozszerzać moduły i zgodnie z jakimi standardami zostały one stworzone

Projekt ma być łatwy do rozszerzenia dla użytkownika generatora, bez konieczności tworzenia zupełnie nowych modułów i wprowadzania nowych standardów.

## 15. Ograniczenia

- brak Kubernetes
- brak TLS
- brak SSO
- brak Nginx
- brak reverse proxy
- brak load balancingu
- brak automatycznego CI/CD
- brak osobnych kontenerów dev i prod
- brak resetu hasła
- brak wysyłki wiadomości email
- brak integracji z dostawcą poczty
