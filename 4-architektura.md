# Architektura

Stan: 16.05.2026

## 1. Wstęp

### 1.1 Cel dokumentu

Dokument przedstawia architekturę generatora oraz najważniejsze decyzje projektowe. Nie narzuca szczegółów technicznych implementacji, ale narzuca podział odpowiedzialności.

### 1.2 Architektura w skrócie

Skrócony przepływ od uruchomienia generatora do gotowego projektu:

1. Użytkownik definiuje, jaki projekt chce otrzymać.
2. Generator zamienia to na konfigurację.
3. Konfiguracja zostaje walidowana.
4. Generator wybiera pasujące template packi.
5. Z template packów powstaje plan generacji.
6. Projekt powstaje w katalogu roboczym.
7. Projekt jest testowany.
8. Projekt trafia do finalnego katalogu.

### 1.3 Najważniejsze założenia architektoniczne

1. Frontend jest niezależny od backendu
   To założenie wymusza komunikację frontendu i backendu jedynie przez API. Oprócz spełnienia podstawowego rozdzielenia odpowiedzialności, pozwoli to autorom rozszerzeń dodawać obsługę nowych frameworków frontendowych w bardzo łatwy sposób, bez wiedzy o całej reszcie za wyjątkiem kontraktu API.
2. Backend i baza danych traktowane są jako backend-db stack
   Być może na papierze ładnie wyglądałoby pełne rozdzielenie backendu i bazy danych. Jednak baza danych w takim projekcie nie jest wyłącznie schemą zapisaną w SQL. W rzeczywistości backend wpływa na ORM, migracje, modele, auth, seedowanie, tabele techniczne i sposób testowania komunikacji z bazą. Dlatego, żeby całość pozostała w pełni natywna dla frameworków backendowych, będę traktował backend i bazę danych jako nierozerwalną całość - kosztem pewnego złamania DRY.
3. W podstawowym zakresie pracy PostgreSQL jest stałą infrastrukturą
   Nie wprowadzę obsługi innych baz danych, jak na przykład SQLite albo MariaDB. Żeby to było możliwe, konieczne byłoby obsłużenie większej ilości stacków backendowych. Docelowo, gdyby projekt był rozszerzany, prawdopodobnie pełna macierz konfiguracji i tak nie byłaby osiągnięta. Każdy backend ma swoje najczęściej wybierane bazy danych i to pewnie one byłyby w pierwszej kolejności uzupełnione.
4. Kontrakty zamiast jakichkolwiek adapterów
   Najprostszą drogą do agresywnego współdzielenia logiki między frameworkami byłoby wprowadzenie adapterów. Z perspektywy generowanego projektu takie adaptery są jednak absolutnie bezużyteczne. W tym projekcie nie dawałyby realnej wartości w wygenerowanej aplikacji, bo użytkownik otrzymałby dodatkową warstwę abstrakcji, której nie potrzebuje do dalszego rozwijania projektu. Dlatego, kosztem DRY i bardziej skomplikowanego kodu, świadomie rezygnuję z użycia adapterów pomiędzy różnymi frameworkami.
5. Template packi są jednostką rozszerzalności
   Nowa technologia, na przykład kolejny framework frontendowy lub kolejny stack backend + db powinny być dodawane jako nowy template pack, a nie warunki do core generatora. Core sprawdzi dostępne packi i na tej podstawie będzie walidował konfigurację.
6. Wygenerowany projekt jest samodzielny
   Po jednorazowym wygenerowaniu projekt nie potrzebuje generatora do dalszego funkcjonowania.
7. Idempotentność i staging
   Nieudana generacja nie może zostawić pozostałości w docelowym katalogu. Ponowne uruchomienie generatora dla tej samej konfiguracji powinno prowadzić do tej samej struktury projektu i nie może uszkadzać istniejącego wyniku. Wznowienie powinno następować od ostatniego poprawnie zakończonego kroku.

### 1.4 Relacja architektury do specyfikacji i kryteriów akceptacyjnych

Architektura jest projektowana z myślą o realizacji specyfikacji i spełnieniu wszystkich kryteriów akceptacyjnych. Ocena jej skuteczności będzie dokonywana właśnie na ich podstawie. Jeśli ta architektura zawiera jakiś element, to musi on odpowiadać na problem ze specyfikacji albo kryteriów. Architektura powinna być pod tym względem minimalna: nie rozwiązuje problemów innych niż te wskazane w specyfikacji i nie jest oceniana w inny sposób, niż to wynika z kryteriów akceptacyjnych.

- Plik ze specyfikacją: 2-specyfikacja.md
- Plik z kryteriami akceptacyjnymi: 3-kryteria-akceptacyjne.md

## 2. Słownik pojęć

### Generator

Narzędzie CLI odpowiedzialne za utworzenie szkieletu aplikacji webowej na podstawie kreatora albo pliku konfiguracyjnego.

Generator nie jest częścią wygenerowanej aplikacji. Jego rola kończy się na przygotowaniu projektu, sprawdzeniu jego poprawności i zapisaniu wyniku w katalogu docelowym.

### Wygenerowany projekt / Projekt

Projekt aplikacji webowej utworzony przez generator.

Wygenerowany projekt zawiera frontend, backend, konfigurację Docker Compose, konfigurację środowiskową, testy oraz dokumentację. Po zakończeniu generacji projekt musi być możliwy do uruchomienia bez generatora.

### Konfiguracja

Zestaw danych wejściowych opisujących, jaki projekt ma zostać wygenerowany.

Konfiguracja może pochodzić z kreatora albo z pliku konfiguracyjnego. Zawiera między innymi nazwę projektu, katalog docelowy, wybrany frontend, wybrany backend, bazę danych, porty oraz wartości środowiskowe.

### Kontrakt HTTP API

Zbiór wymagań określających sposób komunikacji pomiędzy frontendem i backendem.

Kontrakt HTTP API definiuje wymagane endpointy, format requestów, format response'ów, statusy HTTP oraz sposób użycia tokena JWT. Dzięki temu frontend nie musi znać konkretnej implementacji backendu i może komunikować się z każdym backendem spełniającym ten sam kontrakt.

### Kontrakt danych backend-db

Zbiór minimalnych wymagań wobec backend-db stacka dotyczących danych wymaganych do działania aplikacji.

Kontrakt danych określa, że backend-db stack musi zapewnić minimalny model użytkownika pozwalający na jednoznaczną identyfikację użytkownika, logowanie za pomocą emaila, weryfikację hasła zapisanego jako hash oraz oznaczenie użytkownika jako aktywnego lub nieaktywnego.

Kontrakt danych nie wymaga identycznej fizycznej struktury tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez wybrany framework.

### Template

Pojedynczy szablon pliku albo fragmentu pliku używany podczas generacji projektu.

Template może opisywać na przykład plik konfiguracyjny, plik źródłowy, test, fragment README.md albo fragment docker-compose.yml. Template nie powinien zawierać logiki wyboru technologii. Wybór technologii odbywa się wcześniej, na poziomie konfiguracji, rejestru template packów i planu generacji.

### Template pack

Zestaw template'ów, konfiguracji i metadanych odpowiadający za wygenerowanie konkretnej części projektu.

Template pack jest podstawową jednostką rozszerzalności generatora. Nowa technologia, na przykład nowy frontend albo nowy backend-db stack, powinna być dodawana jako nowy template pack, a nie jako dodatkowa logika warunkowa w core generatora.

### Manifest template packa

Opis template packa zawierający informacje potrzebne generatorowi do jego użycia.

Manifest określa między innymi typ template packa, obsługiwaną technologię, wymagane kontrakty, zapewniane funkcjonalności, wymagane dane wejściowe, generowane pliki oraz kompatybilność z innymi elementami generatora.

### Template registry

Rejestr dostępnych template packów.

Template registry pozwala generatorowi sprawdzić, jakie template packi są dostępne, które technologie obsługują, z jakimi kontraktami są zgodne i czy mogą zostać użyte dla wybranej konfiguracji. Dzięki temu core generatora nie musi znać szczegółów konkretnych frameworków.

### Backend-db stack

Sprzężona para backendu i bazy danych traktowana jako jedna jednostka generacji.

Backend i baza danych są łączone w backend-db stack, ponieważ wybór backendu wpływa na ORM, migracje, modele, auth, seedowanie, tabele techniczne oraz testowanie komunikacji z bazą. Przykładami backend-db stacków są FastAPI + PostgreSQL oraz Django + PostgreSQL.

### Core

Główna część generatora odpowiedzialna za obsługę procesu generacji.

Core odpowiada za wczytanie konfiguracji, walidację, wybór template packów, zbudowanie planu generacji, uruchomienie pipeline'u, obsługę stanu, staging, finalizację outputu i statystyki. Core nie powinien zawierać szczegółowej logiki konkretnych frameworków.

### Pipeline

Kontrolowany proces generacji projektu podzielony na kolejne kroki.

Pipeline odpowiada za przeprowadzenie generatora od konfiguracji wejściowej do gotowego projektu. Obejmuje między innymi walidację, wybór template packów, budowanie planu generacji, przygotowanie katalogu roboczego, renderowanie template'ów, verification oraz finalizację outputu.

### Pipeline state

Zapisany stan wykonania pipeline'u.

Pipeline state przechowuje informacje o wykonanych krokach, aktualnym statusie generacji, błędach, użytej konfiguracji, hash konfiguracji oraz ścieżkach katalogów roboczych. Dzięki temu generator może wznowić działanie po błędzie od ostatniego poprawnie zakończonego kroku.

### Generation plan

Plan technicznego wykonania generacji utworzony na podstawie konfiguracji i dobranych template packów.

Generation plan określa, jakie template packi zostaną użyte, jakie pliki zostaną wygenerowane, jakie contributions zostaną dodane do plików wspólnych, jakie kroki pipeline'u zostaną wykonane i jakie testy lub komendy verification powinny zostać uruchomione.

### Contribution

Wkład template packa do pliku albo elementu, który jest składany z wielu źródeł.

Contribution jest używane tam, gdzie jeden plik powstaje z informacji dostarczanych przez wiele template packów. Przykładami takich plików są docker-compose.yml, .env.example oraz README.md.

### Staging

Katalog roboczy, w którym generator tworzy projekt przed zapisaniem go do finalnego katalogu.

Staging chroni katalog docelowy przed częściowo wygenerowanym lub uszkodzonym wynikiem. Projekt trafia do final output dopiero po poprawnym zakończeniu wymaganych kroków pipeline'u.

### Final output

Finalny katalog projektu przekazywany użytkownikowi po zakończeniu generacji.

Final output powinien zawierać wyłącznie poprawnie wygenerowany i zweryfikowany projekt. Nieudana generacja nie powinna zostawiać częściowego wyniku w final output.

### Verification

Proces sprawdzania, czy wygenerowany projekt spełnia wymagania.

Verification obejmuje między innymi sprawdzenie uruchomienia projektu przez Docker Compose, działanie kontraktu HTTP API, działanie kontraktu danych, komunikację frontend-backend, komunikację backend-db oraz przejście wymaganych testów.

### Idempotentność

Właściwość generatora oznaczająca, że ponowne uruchomienie dla tej samej konfiguracji nie prowadzi do niespójnego lub częściowo uszkodzonego projektu.

Idempotentność jest szczególnie ważna przy błędach generacji, wznowieniu pipeline'u i ponownym uruchamianiu generatora dla tej samej konfiguracji.

### Deterministyczność

Właściwość generatora oznaczająca, że ta sama konfiguracja powinna prowadzić do takiej samej struktury wygenerowanego projektu.

Deterministyczność dotyczy przede wszystkim struktury katalogów, wygenerowanych plików, dobranych template packów i planu generacji. Wartości losowe, takie jak sekrety, powinny być jawnie zapisane albo generowane w kontrolowany sposób.

## 3. Ogólny model działania generatora

### 3.1 Przepływ od konfiguracji do projektu

### 3.2 Tryb kreatora

### 3.3 Tryb pliku konfiguracyjnego

### 3.4 Główne etapy działania

## 4. Główne zasady architektoniczne

### 4.1 Frontend zależy wyłącznie od kontraktu HTTP API

### 4.2 Backend i baza danych tworzą backend-db stack

### 4.3 PostgreSQL jako stały element infrastruktury

### 4.4 Kontrakty zamiast adapterów

### 4.5 Natywność template packów

### 4.6 Kontrolowane powtórzenia zamiast sztucznych abstrakcji

### 4.7 Wygenerowany projekt nie zależy runtime'owo od generatora

## 5. Podział systemu na główne części

### 5.1 Core

### 5.2 Contracts

### 5.3 Template packs

### 5.4 Planning

### 5.5 Rendering

### 5.6 Output

### 5.7 State

### 5.8 Verification

### 5.9 Statistics

## 6. Core generatora

### 6.1 Odpowiedzialność core

### 6.2 Czego core nie powinien zawierać

### 6.3 Obsługa CLI

### 6.4 Ładowanie konfiguracji

### 6.5 Normalizacja konfiguracji

### 6.6 Walidacja konfiguracji

### 6.7 Budowanie planu generacji

### 6.8 Uruchamianie pipeline'u

## 7. Konfiguracja wejściowa

### 7.1 Minimalny zestaw danych wejściowych

### 7.2 Konfiguracja projektu

### 7.3 Konfiguracja frontendu

### 7.4 Konfiguracja backendu

### 7.5 Konfiguracja bazy danych

### 7.6 Konfiguracja portów

### 7.7 Konfiguracja środowiskowa

### 7.8 Wartości domyślne

### 7.9 Walidacja konfiguracji przed generacją

## 8. Model kontraktów

### 8.1 Rola kontraktów w architekturze

### 8.2 Kontrakt HTTP API

### 8.3 Kontrakt danych

### 8.4 Wersjonowanie kontraktów

### 8.5 Zgodność template packów z kontraktami

### 8.6 Testowanie zgodności z kontraktami

## 9. Template'y i template packi

### 9.1 Rola template'ów

### 9.2 Rola template packów

### 9.3 Template pack jako jednostka rozszerzalności

### 9.4 Manifest template packa

### 9.5 Template'y właścicielskie

### 9.6 Template'y składane

### 9.7 Contributions do plików wspólnych

### 9.8 Ograniczenie logiki w template'ach

## 10. Rodzaje template packów

### 10.1 Frontend pack

### 10.2 Backend-db pack

### 10.3 Infrastructure pack

### 10.4 Common pack

### 10.5 Verification pack

## 11. Wybór template packów

### 11.1 Rejestr template packów

### 11.2 Dobór frontend packa

### 11.3 Dobór backend-db packa

### 11.4 Dobór infrastructure packa

### 11.5 Dobór common packów

### 11.6 Wykrywanie niewspieranych kombinacji

### 11.7 Wykrywanie konfliktów między packami

## 12. Łączenie template packów

### 12.1 Generation plan jako wynik doboru packów

### 12.2 Kolejność generowania elementów projektu

### 12.3 Łączenie plików właścicielskich

### 12.4 Łączenie plików składanych

### 12.5 Składanie docker-compose.yml

### 12.6 Składanie .env i .env.example

### 12.7 Składanie README.md

### 12.8 Obsługa konfliktów plików

## 13. Backend-db stack

### 13.1 Uzasadnienie sprzężenia backendu i bazy danych

### 13.2 FastAPI + PostgreSQL

### 13.3 Django + PostgreSQL

### 13.4 Minimalny kontrakt danych

### 13.5 Rozszerzenia schemy specyficzne dla frameworka

### 13.6 Migracje

### 13.7 Dane startowe lub testowe do logowania

## 14. Pipeline generacji

### 14.1 Rola pipeline'u

### 14.2 Etapy pipeline'u

### 14.3 Walidacja przed zapisem plików

### 14.4 Przygotowanie stagingu

### 14.5 Renderowanie template packów

### 14.6 Post-processing

### 14.7 Verification

### 14.8 Finalizacja outputu

### 14.9 Raportowanie statystyk

## 15. Staging i output

### 15.1 Rola stagingu

### 15.2 Katalog roboczy generacji

### 15.3 Katalog finalny projektu

### 15.4 Zasada braku częściowego wyniku w final output

### 15.5 Finalizacja poprawnej generacji

### 15.6 Czyszczenie po błędzie

## 16. Stan pipeline'u

### 16.1 Rola stanu pipeline'u

### 16.2 Informacje zapisywane w stanie

### 16.3 Hash konfiguracji

### 16.4 Lista ukończonych kroków

### 16.5 Informacja o błędzie

### 16.6 Wznawianie generacji

### 16.7 Zachowanie po zmianie konfiguracji

## 17. Idempotentność i deterministyczność

### 17.1 Idempotentność generacji

### 17.2 Deterministyczność wyniku strukturalnego

### 17.3 Wartości losowe i sekrety

### 17.4 Ponowne uruchomienie dla tej samej konfiguracji

### 17.5 Ochrona przed niespójnym wynikiem

## 18. Walidacja i obsługa błędów

### 18.1 Walidacja danych wejściowych

### 18.2 Walidacja kombinacji technologicznych

### 18.3 Walidacja portów

### 18.4 Walidacja zmiennych środowiskowych

### 18.5 Walidacja ścieżki output_dir

### 18.6 Komunikaty błędów

### 18.7 Przerwanie generacji przed zapisem plików

## 19. Verification

### 19.1 Rola verification

### 19.2 Verification generatora

### 19.3 Verification wygenerowanego projektu

### 19.4 Verification kontraktu HTTP API

### 19.5 Verification kontraktu danych

### 19.6 Verification Docker Compose

### 19.7 Verification testów

### 19.8 Verification macierzy wspieranych kombinacji

## 20. Struktura katalogów generatora

### 20.1 Proponowana struktura główna

### 20.2 Katalog core

### 20.3 Katalog contracts

### 20.4 Katalog template_packs

### 20.5 Katalog verification

### 20.6 Katalog tests

### 20.7 Katalog docs

## 21. Struktura wygenerowanego projektu

### 21.1 Struktura root projektu

### 21.2 Struktura frontendu

### 21.3 Struktura backendu

### 21.4 Pliki środowiskowe

### 21.5 Pliki Docker

### 21.6 README.md

### 21.7 Testy

## 22. Rozszerzalność generatora

### 22.1 Dodanie nowego frontendu

### 22.2 Dodanie nowego backendu

### 22.3 Dodanie nowej bazy danych

### 22.4 Zgodność rozszerzeń z kontraktami

### 22.5 Brak regresji w istniejących kombinacjach

### 22.6 Ograniczenie zmian w core

### 22.7 Dokumentowanie rozszerzeń

## 23. Jakość architektury

### 23.1 SOLID w generatorze

### 23.2 DRY w generatorze

### 23.3 Open/closed principle

### 23.4 Natywność wygenerowanego kodu

### 23.5 Czytelność i samodokumentujący się kod

### 23.6 Granice odpowiedzialności modułów

## 24. Bezpieczeństwo aplikacyjne w zakresie projektu

### 24.1 JWT

### 24.2 Hashowanie haseł

### 24.3 CORS

### 24.4 Zmienne środowiskowe

### 24.5 Zakres bezpieczeństwa poza projektem

## 25. Decyzje i kompromisy architektoniczne

### 25.1 Dlaczego frontend jest niezależny od backendu

### 25.2 Dlaczego backend i baza są sprzężone

### 25.3 Dlaczego PostgreSQL jest stałym elementem infrastruktury

### 25.4 Dlaczego kontrakty zamiast adapterów

### 25.5 Dlaczego dopuszczalne są kontrolowane powtórzenia

### 25.6 Dlaczego wygenerowany projekt nie zależy od generatora

## 26. Powiązanie architektury z kryteriami akceptacyjnymi

### 26.1 Kryteria generatora

### 26.2 Kryteria wspieranych kombinacji

### 26.3 Kryteria wygenerowanego projektu

### 26.4 Kryteria kontraktów

### 26.5 Kryteria idempotentności i wznawiania

### 26.6 Kryteria rozszerzalności

## 27. Elementy poza zakresem architektury
