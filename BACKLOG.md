# Stan

02.11.2026

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
- [ ] Testy integracyjne endpointów rejestracji, logowania i pobrania użytkownika
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
- [ ] Port w docker-compose.yml ze zmiennej BACKEND_PORT z głównego .env (architektura 14.5)
- [ ] Obraz w docker-compose.yml bez stałej nazwy (architektura 8.3)

#### Poprawki

- [ ] Poprawki zgodności i bezpieczeństwa zasugerowane przez czata
- [ ] Porządki w kodzie i dokumentach

### 2. Szkielet całego pipelinu oraz core

#### Ponowny przegląd architektury

- [x] przegląd architektury i próba doszukania się potencjalnych problemów
- [x] doprecyzowanie nazewnictwa i usunięcie ewentualnych rozjazdów
- [x] rozważenie rezygnacji ze State lub State jako nice-to-have (chyba że dosłownie wyniknie z pipelinu, że to jest łatwe: hash konfiigu + zapisanie stanu pipelinu)
- [x] opisanie moich rozważań co do rezygnacji z powodu braku czasu z Reacta (lub zrobienie bardzo bazowego, niekoniecznie dopracowanego template packa) oraz przejścia z Django na ASP.Net

#### Szkielet core

- [x] Obiekty i architektoniczne fundamenty core
- [x] Wykonanywanie planu generacji
- [x] Obsługa pipelinu

#### Konfiguracja

- [x] Format pliku konfiguracyjnego
- [x] Odczyt manifestu
- [x] Normalizacja konifguracji (pełne 6.5)
- [x] Walidacja konfiguracji (pełne 6.6)
- [ ] Obsługa dla Django, by sekret o tej samej nazwie w różnych częściach projektu miał taką samą wartość
- [ ] Sprawdzanie, że każda część ma jednego właściciela i może deklarować envy tylko gdy deklaruje porty
- [x] Pominięcie ładowania, gdy katalog template nie ma katalogu zadeklarowanej części (architektura 13.4)
- [ ] Normalizacja bez łączenia sekretów z kilku manifestów i bez pomijania sekretów części bez portu

#### Pipeline

- [x] Obiekty i architektoniczne fundamenty pipelinu
- [x] Zdefiniowanie każdego z kroków pipelinu w kodzie

#### Plan generacji i generacja

- [x] Określenie formatu planu generacji
- [x] Implementacja planu generacji

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
- [ ] test happy path

### 4. Template pack django

#### Fundament

- [ ] Struktura aplikacji Django
- [ ] Konfiguracja z plików env z walidacją i ochroną sekretów
- [ ] Narzędzia jakości i makefile
- [ ] Baza PostgreSQL, model użytkownika i migracje

#### Kontrakt HTTP API

- [ ] Endpointy health ze sprawdzaniem bazy i migracji
- [ ] Rejestracja, logowanie tokenem JWT i pobranie aktualnego użytkownika
- [ ] Obsługa błędów zgodna z formatem kontraktu

#### Testy

- [ ] Testy jednostkowe i integracyjne backend-db
- [ ] Testy integracyjne endpointów rejestracji, logowania i pobrania użytkownika

#### Uruchomienie i forma template packa

- [ ] Docker Compose z usługą bazy, migracjami i healthcheckiem
- [ ] README z instrukcją uruchomienia
- [ ] Manifest i wkład packa do wspólnych plików projektu

### 5. Ukończenie generatora

#### Testy generatora, potem testy razem z implementacją

- [ ] Testy wczytywania konfiguracji
- [ ] Testy normalizacji konfiguracji
- [ ] Testy walidacji konfiguracji
- [ ] Testy tworzenia generation planu
- [ ] Testy kontraktów wywoływane z generatora

#### Pozostałe

- [ ] Format i sklejanie plików contributions: zasady
- [ ] Procedura cleanupu stagingu
- [ ] Cleanup po błędzie w kroku, po ctrl+c oraz na początku uruchomienia, jeśli katalog nie jest pusty
- [ ] Dokumentacja generatora

#### Implementacja budujących kroków pipelinu

- [ ] Pipeline krok 1
- [ ] Pipeline krok 2
- [ ] Pipeline krok 3
- [ ] Pipeline krok 4

#### Implementacja pozostałych kroków pipelinu

- [ ] Pipeline krok 5
- [ ] Pipeline krok 6
- [ ] Pipeline krok 7
- [ ] Pipeline krok 8
- [ ] Pipeline krok 9
- [ ] Pipeline krok 10
- [ ] Pipeline krok 11
- [ ] Pipeline krok 12
- [ ] Pipeline krok 13
- [ ] Pipeline krok 14

#### CLI

- [ ] Wybór frameworka pod CLI. Sprawdzenie go i przetestowanie możliwości
- [ ] Zebranie danych wejściowych od użytkownika
- [ ] Zapis odpowiedzi kreatora jako plik konfiguracyjny
- [ ] Obsługa przejścia przez cały proces przez CLI
- [ ] Flaga --force

#### Statistics

- [ ] Model statystyk
- [ ] Zbieranie statystyk kroków poza pipelinem
- [ ] Zbieranie statystyk kroków pipeline'u
- [ ] Wyświetlenie statystyk w CLI jako ostanti krok

### 6. Stworzenie pracy inżynierskiej

- [ ] napisanie tekstu pracy w md
- [ ] przeniesienie pracy na docelowy format w latechu
- [ ] zrobienie wszystkiego co konieczne przed złożeniem pracy

### 7. Template pack reacta
