# Zmiany zakresu

Stan: 31.10.2026

## 1 Cel dokumentu

Dokument powstaje, by uzasadnić zmiany projektowe oraz zmiany dotyczące zakresu pracy. Głównym powodem jest pozostały czas oraz potrzeba uspójnienia dokumentacji, która pojawiła się podczas implementacji.

## 2 Zakres zmian

Elementy, które zostaną zmienione:

- State i wznawialność
- Zakres template packów
- Spójność nazewnictwa

## 3 State

### 3.1 Decyzja

Każde uruchomienie generatora zaczyna od zera w nowym stagingu. Po błędzie generator sprząta cały run na raz, a nie każdy krok osobno.

### 3.2 Koszt wznawiania

Zapis hasha konfiguracji i listy ukończonych kroków to tylko mała część wznawiania. Pozostała część to:

- sekrety: normalizacja losuje brakujące sekrety, więc hash znormalizowanej konfiguracji jest przy każdym uruchomieniu inny. Wznawianie wymaga hashowania konfiguracji przed normalizacją i zapisu wylosowanych sekretów w pliku stanu
- zmiany template packów: poprawka w template packu między uruchomieniami unieważnia wyrenderowane pliki, więc hash musiałby obejmować także zawartość template packów
- uzgadnianie stanu: po przerwaniu procesu cleanup się nie wykonuje. Przed wznowieniem generator musiałby porównać zapisany stan z faktycznym stanem stagingu i kontenerów Docker
- CLI: tryb wznowienia, wybór runa i sprzątanie starych runów
- testy: automatyczna weryfikacja wymaga wymuszenia błędu na granicy każdego kroku, w tym kroków korzystających z Dockera

### 3.3 Zysk ze wznawiania

- rendering trwa sekundy, a najdłuższe kroki, czyli build obrazów i testy, są na końcu pipeline'u
- build obrazów korzysta z cache warstw Dockera, który działa niezależnie od generatora
- błąd weryfikacji to zwykle błąd template packa, po którego poprawce projekt i tak trzeba wyrenderować od nowa, albo błąd środowiska, przy którym wznowienie oszczędza tylko czas renderingu

Jedynym realnym zyskiem jest brak ponownego przechodzenia przez kreator. Nie wymaga to stanu, wystarczy zapis odpowiedzi z kreatora jako plik konfiguracyjny, z którym można ponownie uruchomić generator.

## 4 Zakres template packów

### 4.1 Decyzja

Generator wspiera dwie kombinacje: Nuxt + FastAPI + SQLite oraz Nuxt + Django + PostgreSQL. React nie wchodzi do zakresu, a drugim backend-db stackiem jest Django + PostgreSQL, a nie ASP.NET Core + PostgreSQL.

### 4.2 Uzasadnienie

- czas: pack FastAPI zajął 6 dni pracy, a do końca grudnia oprócz niego muszę skończyć generator, pack Nuxta i Django. Jako że pracę piszę głównie w weekendy, to czasu wcale nie mam aż tak dużo
- drugi backend zamiast drugiego frontendu: frontend zależy wyłącznie od kontraktu HTTP API, więc drugi frontend najmniej sprawdza generator. Drugi backend-db stack sprawdza bazę danych jako osobną usługę, sekrety używane przez kilka usług i niezależność kontraktu API od frameworka, więc lepiej dopracować drugi backend-db stack, niż włożyć ten czas we frontend
- Django zamiast ASP.NET Core: generator nie uruchamia kodu projektu lokalnie i komunikuje się z template packami wyłącznie przez manifest i Dockera, więc język backendu ma dla niego małe znaczenie. Nową ścieżką w pipelinie jest PostgreSQL jako osobna usługa, a nie język
- dwie kombinacje wystarczą, żeby rozszerzalność pokazać w praktyce: dodanie Django nie może wymagać zmian w template packu Nuxta ani w core

## 5 Spójność nazewnictwa

### 5.1 Decyzja

Ujednoliciłem nazwy w całej dokumentacji, żeby każde pojęcie miało jedną nazwę i jedno znaczenie:

- generator szkieletów aplikacji webowych, a nie szablonów, bo szablon to template
- katalog docelowy to katalog podany w project.output_dir, a katalog projektu to katalog o nazwie project.name w jego środku
- część projektu to frontend, backend albo database, a usługa i kontener dotyczą tylko Dockera
- kreator to jeden z dwóch trybów CLI, a nie całe CLI
- walidacja to wszystkie sprawdzenia przed generacją, a weryfikacja to testowanie projektu w stagingu
- etap to jeden z siedmiu etapów generacji, a krok to krok pipeline'u
- template całościowy daje plik całościowy, a template częściowy (contribution) fragment pliku składanego
- template pack ma typ frontend albo backend-db
- sekret to wymagana zmienna środowiskowa, którą generator losuje, jeśli użytkownik jej nie poda
- nazwy piszę po polsku, a po angielsku zostają tylko ustalone terminy: core, pipeline, staging, cleanup, output, run, template, template pack, contribution, manifest, backend-db stack i happy path

### 5.2 Zmiany projektowe

Przy przeglądzie wyszło kilka miejsc, w których dokumenty nie tylko różnie nazywały rzeczy, ale opisywały różne rozwiązania. Rozstrzygnąłem je tak:

- są tylko dwa typy template packów, bez osobnego packa konteneryzacji, bo konfiguracja wskazuje tylko frontend i backend, a Dockerfile i tak są w packach
- wartości z konfiguracji trafiają do projektu wyłącznie przez pliki .env, więc template pack zostaje działającą aplikacją, którą da się uruchomić bez generatora
- pipeline ma stałą listę kroków, a plan generacji tylko ją parametryzuje
- test happy path jest we frontendzie, a wspólne testy kontraktu w generatorze, więc oba piszę raz i sprawdzają każdy backend
- niepusty katalog projektu i zajęty port w trybie pliku konfiguracyjnego przechodzą tylko z flagą `--force`
