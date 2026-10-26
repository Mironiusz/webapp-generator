# Stan

17.10.2026

## Po co

Te pliki pozwolą mi łatwiej układać sobie pracę krok po kroku i dzielić ją na nieco mniejsze wersje, będące checkpointami. Dzięki temu będę mógł łatwiej niż tylko porównując ze spec i KA oszacować, ile jeszcze zostało mi do zrobienia i czy mogę na przykład zrobić coś więcej.

## Zakres

### 1. Template pack fastapi

#### Fundament

- [x] Struktura aplikacji z podziałem na warstwy
- [x] Konfiguracja z plików env z walidacją i ochroną sekretów
- [x] Narzędzia jakości i makefile
- [x] Asynchroniczna baza SQLite, model użytkownika i migracje

#### Kontrakt HTTP API

- [x] Endpointy health ze sprawdzaniem bazy i migracji
- [x] Rejestracja z walidacją i hashowaniem haseł
- [x] Logowanie tokenem JWT i pobranie aktualnego użytkownika
- [x] Obsługa błędów, dokumentacja OpenAPI i CORS

#### Testy

- [x] Podstawowe testy jednostkowe konfiguracji by coś przechodziło `make check`
- [ ] Testy jednostkowe i integracyjne backend-db
- [ ] Test dymny rejestracji, logowania i pobrania użytkownika
- [ ] Uruchamianie testów w kontenerach

#### Uruchomienie i dokumentacja

- [x] Obraz Docker bez zbędnych plików, uruchamiany jako nie-root
- [x] Docker Compose z migracjami, trwałą bazą i healthcheckiem
- [x] README z instrukcją uruchomienia
- [ ] Uzupełnienie README o strukturę, rozszerzanie i komendy

#### Forma template packa

- [x] Manifest i parametry dla generatora
- [ ] Wkład packa do wspólnych plików projektu
- [ ] Wykluczenie plików sandboxa

#### Poprawki

- [ ] Poprawki zgodności i bezpieczeństwa zasugerowane przez czata
- [ ] Porządki w kodzie i dokumentach

### 2. Szkielet całego pipelinu oraz core

#### Ponowny przegląd architektury

- [ ] przegląd architektury i próba doszukania się potencjalnych problemów
- [ ] doprecyzowanie nazewnictwa i usunięcie ewentualnych rozjazdów
- [ ] rozważenie rezygnacji ze State lub State jako nice-to-have (chyba że dosłownie wyniknie z pipelinu, że to jest łatwe: hash konfiigu + zapisanie stanu pipelinu)
- [ ] opisanie moich rozważań co do rezygnacji z powodu braku czasu z Reacta (lub zrobienie bardzo bazowego, niekoniecznie dopracowanego template packa) oraz przejścia z Django na ASP.Net

#### Szkielet core

- [x] Obiekty i architektoniczne fundamenty core
- [ ] Korzystanie z CLI i obserwowalność
- [ ] Wykonanywanie planu generacji
- [ ] Obsługa pipelinu

#### Konfiguracja

- [x] Format pliku konfiguracyjnego
- [x] Odczyt manifestu
- [ ] Normalizacja konifguracji (pełne 6.5)
- [ ] Walidacja konfiguracji (pełne 6.6)

#### CLI

- [ ] Wybór frameworka pod CLI. Sprawdzenie go i przetestowanie możliwości
- [ ] Zebranie danych wejściowych od użytkownika
- [ ] Obsługa przejścia przez cały proces przez CLI, na mockach

#### Pipeline

- [ ] Zdefiniowanie każdego z kroków pipelinu w kodzie
- [ ] Obiekty i architektoniczne fundamenty pipelinu

#### Plan generacji i generacja

- [ ] Określenie formatu planu generacji
- [ ] Wykonywalność planu generacji

#### Weryfikacja i finalizacja

- [ ] Procedura weryfikacyjna ze stagingiem
- [ ] Procedura finalizacji
- [ ] Wygenerowany backend wstaje przez docker compose

### 3. Template pack nuxta

#### Fundament

- [ ] nowy projekt Nuxta
- [ ] wybór docelowego układu plików i modułów
- [ ] routing

#### Strony bez backendu

- [ ] strona logowania
- [ ] strona rejestracji
- [ ] strona aplikacji
- [ ] strona 404

#### Integracja z backendem

- [ ] integracja stron z backendem
- [ ] obsługa tokena JWT
- [ ] obsługa błędu logowania

#### Testy

- [ ] testy jednostkowe
- [ ] testy integracyjne

### 4. Ukończenie generatora

### 5. Stworzenie pracy inżynierskiej

- [ ] napisanie tekstu pracy w md
- [ ] przeniesienie pracy na docelowy format w latechu
- [ ] zrobienie wszystkiego co konieczne przed złożeniem pracy

### 6. Dodanie kolejnych dwóch template packów

- [ ] React
- [ ] ASP.Net
