# Specyfikacja

Stan: 16.05.2026

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
- backend
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
- ports.database
- env

## 6. Wspierane technologie i kombinacje

Generator musi wspierać następujące kombinacje:

- Vue + FastAPI + PostgreSQL
- React + FastAPI + PostgreSQL
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

```
frontend/
backend/
docker-compose.yml
.env
.env.example
.gitignore
.dockerignore
README.md
```

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
- strona aplikacji
- strona 404
- klient HTTP do backendu
- obsługa tokena JWT
- obsługa błędu logowania
- testy jednostkowe
- testy integracyjne

### 9.2 Backend

- endpoint health
- endpoint login
- endpoint zwracający dane aktualnego użytkownika
- obsługa CORS
- obsługa JWT
- testy jednostkowe
- testy integracyjne

### 9.3 Baza danych

Baza danych jest w PostgreSQL.

Backend zapewnia:

- migracje
- minimalny model użytkownika
- dane wymagane do sprawdzenia logowania

### 9.4 Komunikacja

- działa komunikacja frontend-backend
- działa komunikacja backend-db

"Działanie" definiuję przejściem testów integracyjnych.

## 10. Kontrakt HTTP API

### 10.1 GET /health

Endpoint służy do sprawdzenia, czy backend działa.

#### Response 200

```json
{
	"status": "ok"
}
```

#### Response 500

```json
{
	"detail": "Service unavailable"
}
```

### 10.2 POST /auth/login

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
	"access_token": "string",
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

```json
{
	"detail": "Invalid credentials"
}
```

### 10.3 GET /auth/me

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
	"email": "admin@example.com",
	"is_active": true
}
```

#### Response 401

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
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

Kontrakt danych nie wymaga identycznej fizycznej struktury wszystkich tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez framework.

## 12. Wymagania środowiskowe

Środowiskiem wygenerowanego projektu będzie zbiór kontenerów Docker. Projekt uruchamiany jest przez:

```
docker compose up -d --build
```

Powstaną trzy kontenery:

- backend
- frontend
- database

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
- testy wygenerowanego projektu

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

- jedyna wspierana baza danych to PostgreSQL
- brak Kubernetes
- brak TLS
- brak SSO
- brak Nginx
- brak reverse proxy
- brak load balancingu
- brak automatycznego CI/CD
- brak osobnych kontenerów dev i prod
