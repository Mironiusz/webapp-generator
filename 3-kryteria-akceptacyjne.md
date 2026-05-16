# Kryteria akceptacyjne

Stan: 16.05.2026

## 1. Cel dokumentu

Dokument określa warunki, które muszą zostać spełnione, aby projekt generatora szablonów aplikacji webowych można było uznać za poprawnie zrealizowany.

Kryteria akceptacyjne wynikają ze specyfikacji projektu i służą do weryfikacji działania generatora oraz jakości wygenerowanych projektów.

## 2. Zasada akceptacji projektu

Projekt zostaje uznany za zaakceptowany, jeśli:

- generator poprawnie tworzy projekt dla każdej wspieranej kombinacji technologicznej
- wygenerowany projekt uruchamia się przez Docker Compose
- wygenerowana aplikacja spełnia kontrakt HTTP API
- backend-db stack spełnia minimalny kontrakt danych
- testy automatyczne przechodzą dla każdej wspieranej kombinacji
- generator poprawnie obsługuje błędne dane wejściowe
- wygenerowany projekt jest możliwy do dalszego rozszerzania przez użytkownika

## 3. Typy weryfikacji

Kryteria mogą być weryfikowane na trzy sposoby:

- automatycznie - przez testy, skrypty, uruchomienie komend albo sprawdzenie outputu
- ręcznie - przez ocenę struktury, dokumentacji i jakości kodu
- automatycznie i ręcznie - gdy część kryterium można sprawdzić testem, ale część wymaga oceny jakościowej

## 4. Kryteria dla generatora

### KA-GEN-01 - Uruchomienie generatora jako narzędzia CLI

Kryterium jest spełnione, jeśli generator można uruchomić jako narzędzie CLI.

Typ weryfikacji: automatyczna.

### KA-GEN-02 - Generowanie projektu z kreatora

Kryterium jest spełnione, jeśli użytkownik może przejść przez kreator, podać wymagane dane i wygenerować projekt.

Typ weryfikacji: automatyczna i ręczna.

### KA-GEN-03 - Generowanie projektu z pliku konfiguracyjnego

Kryterium jest spełnione, jeśli generator potrafi utworzyć projekt bez interakcji z użytkownikiem, wyłącznie na podstawie pliku konfiguracyjnego.

Typ weryfikacji: automatyczna.

### KA-GEN-04 - Walidacja konfiguracji przed generacją

Kryterium jest spełnione, jeśli generator sprawdza poprawność konfiguracji przed rozpoczęciem zapisu plików projektu.

Typ weryfikacji: automatyczna.

### KA-GEN-05 - Raportowanie statystyk

Kryterium jest spełnione, jeśli po zakończeniu generacji generator zwraca podstawowe statystyki, w szczególności czas generacji oraz informację o wybranej kombinacji technologicznej.

Typ weryfikacji: automatyczna i ręczna.

## 5. Kryteria dla wspieranych kombinacji technologicznych

### KA-STACK-01 - Vue + FastAPI + PostgreSQL

Kryterium jest spełnione, jeśli generator tworzy działający projekt dla kombinacji Vue + FastAPI + PostgreSQL.

Typ weryfikacji: automatyczna.

### KA-STACK-02 - React + FastAPI + PostgreSQL

Kryterium jest spełnione, jeśli generator tworzy działający projekt dla kombinacji React + FastAPI + PostgreSQL.

Typ weryfikacji: automatyczna.

### KA-STACK-03 - Vue + Django + PostgreSQL

Kryterium jest spełnione, jeśli generator tworzy działający projekt dla kombinacji Vue + Django + PostgreSQL.

Typ weryfikacji: automatyczna.

### KA-STACK-04 - React + Django + PostgreSQL

Kryterium jest spełnione, jeśli generator tworzy działający projekt dla kombinacji React + Django + PostgreSQL.

Typ weryfikacji: automatyczna.

### KA-STACK-05 - Brak obsługi niewspieranych kombinacji

Kryterium jest spełnione, jeśli generator odrzuca konfigurację zawierającą kombinację technologiczną spoza listy wspieranych kombinacji.

Typ weryfikacji: automatyczna.

## 6. Kryteria dla wygenerowanego projektu

### KA-OUT-01 - Struktura katalogu wynikowego

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera co najmniej:

```text
frontend/
backend/
docker-compose.yml
.env
.env.example
.gitignore
.dockerignore
README.md
```

Typ weryfikacji: automatyczna.

### KA-OUT-02 - Samodzielność wygenerowanego projektu

Kryterium jest spełnione, jeśli wygenerowany projekt można uruchomić bez generatora.

Typ weryfikacji: automatyczna.

### KA-OUT-03 - Dokumentacja wygenerowanego projektu

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera README.md opisujące:

- sposób uruchomienia projektu
- strukturę projektu
- sposób rozszerzania frontendu
- sposób rozszerzania backendu
- podstawowe komendy developerskie i testowe

Typ weryfikacji: ręczna.

## 7. Kryteria dla środowiska Docker

### KA-DOCKER-01 - Uruchomienie projektu przez Docker Compose

Kryterium jest spełnione, jeśli projekt można uruchomić komendą:

```bash
docker compose up -d --build
```

Typ weryfikacji: automatyczna.

### KA-DOCKER-02 - Wymagane kontenery

Kryterium jest spełnione, jeśli po uruchomieniu projektu działają kontenery:

- frontend
- backend
- database

Typ weryfikacji: automatyczna.

### KA-DOCKER-03 - Konfiguracja środowiskowa

Kryterium jest spełnione, jeśli projekt zawiera pliki .env i .env.example, a wartości w .env umożliwiają uruchomienie projektu bez dodatkowej konfiguracji.

Typ weryfikacji: automatyczna i ręczna.

### KA-DOCKER-04 - Zatrzymanie projektu

Kryterium jest spełnione, jeśli projekt można zatrzymać komendą:

```bash
docker compose down
```

Typ weryfikacji: automatyczna.

## 8. Kryteria dla kontraktu HTTP API

### KA-API-01 - Endpoint GET /health

Kryterium jest spełnione, jeśli endpoint GET /health zwraca status HTTP 200 oraz odpowiedź:

```json
{
	"status": "ok"
}
```

Typ weryfikacji: automatyczna.

### KA-API-02 - Endpoint POST /auth/login dla poprawnych danych

Kryterium jest spełnione, jeśli endpoint POST /auth/login dla poprawnych danych logowania zwraca status HTTP 200 oraz odpowiedź zawierającą access_token i token_type.

Oczekiwany format odpowiedzi:

```json
{
	"access_token": "string",
	"token_type": "bearer"
}
```

Typ weryfikacji: automatyczna.

### KA-API-03 - Endpoint POST /auth/login dla niepoprawnych danych

Kryterium jest spełnione, jeśli endpoint POST /auth/login dla niepoprawnych danych logowania zwraca status HTTP 401.

Typ weryfikacji: automatyczna.

### KA-API-04 - Endpoint GET /auth/me bez tokena

Kryterium jest spełnione, jeśli endpoint GET /auth/me bez tokena JWT zwraca status HTTP 401.

Typ weryfikacji: automatyczna.

### KA-API-05 - Endpoint GET /auth/me z poprawnym tokenem

Kryterium jest spełnione, jeśli endpoint GET /auth/me z poprawnym tokenem JWT zwraca status HTTP 200 oraz dane aktualnego użytkownika.

Oczekiwany format odpowiedzi:

```json
{
	"id": 1,
	"email": "admin@example.com",
	"is_active": true
}
```

Typ weryfikacji: automatyczna.

### KA-API-06 - Spójność API między backendami

Kryterium jest spełnione, jeśli backend FastAPI i backend Django zwracają odpowiedzi zgodne z tym samym kontraktem HTTP API.

Typ weryfikacji: automatyczna.

## 9. Kryteria dla kontraktu danych

### KA-DATA-01 - Minimalny model użytkownika

Kryterium jest spełnione, jeśli backend-db stack zapewnia minimalny model użytkownika pozwalający na:

- jednoznaczną identyfikację użytkownika
- logowanie za pomocą emaila
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

Typ weryfikacji: automatyczna i ręczna.

### KA-DATA-02 - Migracje bazy danych

Kryterium jest spełnione, jeśli migracje bazy danych uruchamiają się poprawnie i tworzą struktury wymagane do działania logowania.

Typ weryfikacji: automatyczna.

### KA-DATA-03 - Dane wymagane do sprawdzenia logowania

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera sposób utworzenia użytkownika testowego albo startowego pozwalającego sprawdzić logowanie.

Typ weryfikacji: automatyczna.

### KA-DATA-04 - Dodatkowe tabele frameworka

Kryterium jest spełnione, jeśli backend może posiadać dodatkowe tabele techniczne wymagane przez framework, ale nie narusza to minimalnego kontraktu danych.

Typ weryfikacji: ręczna.

## 10. Kryteria dla komunikacji między modułami

### KA-COMM-01 - Komunikacja frontend-backend

Kryterium jest spełnione, jeśli frontend potrafi wykonać zapytanie do backendu i obsłużyć odpowiedź zgodną z kontraktem HTTP API.

Typ weryfikacji: automatyczna.

### KA-COMM-02 - Komunikacja backend-db

Kryterium jest spełnione, jeśli backend potrafi połączyć się z bazą PostgreSQL i wykonać operację wymaganą do działania logowania.

Typ weryfikacji: automatyczna.

## 11. Kryteria dla testów

### KA-TEST-01 - Testy jednostkowe backendu

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera i uruchamia testy jednostkowe backendu.

Typ weryfikacji: automatyczna.

### KA-TEST-02 - Testy jednostkowe frontendu

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera i uruchamia testy jednostkowe frontendu.

Typ weryfikacji: automatyczna.

### KA-TEST-03 - Testy integracyjne backend-db

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera testy potwierdzające działającą komunikację backendu z bazą danych.

Typ weryfikacji: automatyczna.

### KA-TEST-04 - Testy integracyjne frontend-backend

Kryterium jest spełnione, jeśli wygenerowany projekt zawiera testy potwierdzające działającą komunikację frontendu z backendem.

Typ weryfikacji: automatyczna.

### KA-TEST-05 - Testy wygenerowanego projektu

Kryterium jest spełnione, jeśli wygenerowany projekt posiada jeden udokumentowany sposób uruchomienia całego zestawu testów.

Typ weryfikacji: automatyczna i ręczna.

## 12. Kryteria dla idempotentności i wznawiania

### KA-IDEMP-01 - Ponowne uruchomienie generatora

Kryterium jest spełnione, jeśli ponowne uruchomienie generatora dla tej samej konfiguracji nie prowadzi do niespójnego lub częściowo uszkodzonego projektu.

Typ weryfikacji: automatyczna.

### KA-IDEMP-02 - Wznowienie po błędzie

Kryterium jest spełnione, jeśli po błędzie generator umożliwia wznowienie generacji od ostatniego poprawnie zakończonego etapu.

Typ weryfikacji: automatyczna i ręczna.

### KA-IDEMP-03 - Brak częściowego wyniku w katalogu finalnym

Kryterium jest spełnione, jeśli nieudany etap generacji nie pozostawia częściowo wygenerowanego projektu w katalogu finalnym.

Typ weryfikacji: automatyczna.

### KA-IDEMP-04 - Zmiana konfiguracji a wznowienie

Kryterium jest spełnione, jeśli generator nie wznawia bezrefleksyjnie poprzedniej generacji po zmianie konfiguracji wejściowej.

Typ weryfikacji: automatyczna.

## 13. Kryteria negatywne

### KA-NEG-01 - Niewspierany frontend

Kryterium jest spełnione, jeśli podanie niewspieranego frontendu kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

### KA-NEG-02 - Niewspierany backend

Kryterium jest spełnione, jeśli podanie niewspieranego backendu kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

### KA-NEG-03 - Niewspierana baza danych

Kryterium jest spełnione, jeśli podanie bazy danych innej niż PostgreSQL kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

### KA-NEG-04 - Konflikt portów

Kryterium jest spełnione, jeśli konflikt portów kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

### KA-NEG-05 - Brak wymaganych danych wejściowych

Kryterium jest spełnione, jeśli brak wymaganych danych wejściowych kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

### KA-NEG-06 - Niepoprawna ścieżka output_dir

Kryterium jest spełnione, jeśli niepoprawna ścieżka output_dir kończy się błędem walidacji.

Typ weryfikacji: automatyczna.

## 14. Kryteria jakościowe

### KA-QUALITY-01 - Zgodność z SOLID

Kryterium jest spełnione, jeśli wygenerowany kod jest ręcznie oceniony jako zgodny z zasadami SOLID w zakresie uzasadnionym dla wygenerowanego szkieletu aplikacji.

Typ weryfikacji: ręczna.

### KA-QUALITY-02 - Zgodność z DRY

Kryterium jest spełnione, jeśli wygenerowany kod nie zawiera nieuzasadnionych powtórzeń, a ewentualne powtórzenia wynikają z potrzeby zachowania natywności danej technologii.

Typ weryfikacji: ręczna.

### KA-QUALITY-03 - Czytelność kodu

Kryterium jest spełnione, jeśli wygenerowany kod jest czytelny, podzielony na logiczne moduły i możliwy do dalszego rozszerzania.

Typ weryfikacji: ręczna.

### KA-QUALITY-04 - Dokumentowanie kodu

Kryterium jest spełnione, jeśli funkcje wymagające wyjaśnienia posiadają docstringi, a kod nie opiera się na komentarzach linijkowych jako głównym sposobie dokumentowania logiki.

Typ weryfikacji: ręczna.

### KA-QUALITY-05 - Dokumentacja rozszerzania projektu

Kryterium jest spełnione, jeśli README.md opisuje, jak użytkownik może rozszerzać wygenerowany frontend i backend.

Typ weryfikacji: ręczna.

## 15. Kryteria rozszerzalności generatora

### KA-EXT-01 - Dokumentacja sposobu dodawania nowej technologii

Kryterium jest spełnione, jeśli dokumentacja generatora opisuje, jakie elementy należy dodać, aby rozszerzyć generator o nowy frontend albo backend.

Typ weryfikacji: ręczna.

### KA-EXT-02 - Dodanie nowego frontendu bez modyfikowania backendów

Kryterium jest spełnione, jeśli architektura generatora umożliwia dodanie nowego frontendu bez konieczności modyfikowania istniejących backendów oraz istniejących kombinacji technologicznych.

Nowy frontend musi komunikować się z backendem wyłącznie przez kontrakt HTTP API.

Typ weryfikacji: ręczna.

### KA-EXT-03 - Dodanie nowego backendu bez modyfikowania frontendów

Kryterium jest spełnione, jeśli architektura generatora umożliwia dodanie nowego backendu bez konieczności modyfikowania istniejących frontendów oraz istniejących kombinacji technologicznych.

Nowy backend musi spełniać kontrakt HTTP API oraz minimalny kontrakt danych.

Typ weryfikacji: ręczna.

### KA-EXT-04 - Brak wpływu rozszerzenia na istniejące kombinacje

Kryterium jest spełnione, jeśli dodanie obsługi nowej technologii nie powoduje regresji w istniejących wspieranych kombinacjach technologicznych.

Typ weryfikacji: automatyczna i ręczna.

### KA-EXT-05 - Jawne wymagania dla rozszerzenia

Kryterium jest spełnione, jeśli nowa technologia musi jawnie określić:

- jakie pliki generuje
- jakie dane wejściowe wykorzystuje
- jakie kontrakty spełnia
- jakie testy powinny potwierdzić jej poprawność
- z jakimi elementami generatora jest kompatybilna

Typ weryfikacji: ręczna.

### KA-EXT-06 - Zgodność rozszerzenia z kontraktami

Kryterium jest spełnione, jeśli każde rozszerzenie dodające nowy frontend albo backend musi być zgodne z istniejącymi kontraktami projektu.

Dla frontendu oznacza to zgodność z kontraktem HTTP API.

Dla backendu oznacza to zgodność z kontraktem HTTP API oraz minimalnym kontraktem danych.

Typ weryfikacji: automatyczna i ręczna.

### KA-EXT-07 - Ograniczenie zmian w core generatora

Kryterium jest spełnione, jeśli dodanie nowej technologii nie wymaga istotnych zmian w głównej logice generatora odpowiedzialnej za konfigurację, walidację, generację i weryfikację.

Dopuszczalne są zmiany rejestrujące nowe rozszerzenie albo aktualizujące listę wspieranych technologii.

Typ weryfikacji: ręczna.

### KA-EXT-08 - Rozszerzalność bez sztucznych abstrakcji

Kryterium jest spełnione, jeśli mechanizm rozszerzeń pozwala zachować natywność danej technologii i nie wymusza tworzenia wspólnej struktury kodu dla frameworków, które naturalnie działają inaczej.

Typ weryfikacji: ręczna.

## 16. Warunek końcowej akceptacji

Projekt zostaje uznany za zaakceptowany, jeśli:

- spełnione są wszystkie kryteria dotyczące generatora
- spełnione są wszystkie kryteria dotyczące wspieranych kombinacji technologicznych
- spełnione są wszystkie kryteria dotyczące wygenerowanego projektu
- spełnione są wszystkie kryteria dotyczące kontraktu HTTP API
- spełnione są wszystkie kryteria dotyczące kontraktu danych
- spełnione są wszystkie kryteria dotyczące komunikacji między modułami
- spełnione są wszystkie kryteria dotyczące testów
- spełnione są wszystkie kryteria dotyczące idempotentności i wznawiania
- spełnione są wszystkie kryteria negatywne
- spełnione są wszystkie kryteria dotyczące rozszerzalności generatora
- kryteria jakościowe zostały pozytywnie ocenione ręcznie
