# Architektura

Stan: 31.10.2026

## 1 Wstęp

### 1.1 Cel dokumentu

Dokument przedstawia architekturę generatora oraz najważniejsze decyzje projektowe. Nie narzuca szczegółów technicznych implementacji, ale narzuca podział odpowiedzialności.

### 1.2 Architektura w skrócie

Skrócony przepływ od uruchomienia generatora do gotowego projektu:

1. Użytkownik definiuje, jaki projekt chce otrzymać, a generator wczytuje to jako konfigurację i sprawdza, czy wskazane template packi istnieją.
2. Konfiguracja zostaje znormalizowana i uzupełniona o wartości domyślne z manifestów template packów.
3. Konfiguracja zostaje zwalidowana.
4. Powstaje plan generacji.
5. Projekt powstaje w katalogu roboczym.
6. Projekt jest weryfikowany testami.
7. Projekt trafia do katalogu docelowego.

### 1.3 Najważniejsze założenia architektoniczne

1. Frontend jest niezależny od backendu
   To założenie wymusza komunikację frontendu i backendu jedynie przez API. Oprócz spełnienia podstawowego rozdzielenia odpowiedzialności, pozwoli to autorom rozszerzeń dodawać obsługę nowych frameworków frontendowych w bardzo łatwy sposób, bez wiedzy o całej reszcie za wyjątkiem kontraktu API.
2. Backend i baza danych traktowane są jako backend-db stack
   Być może na papierze ładnie wyglądałoby pełne rozdzielenie backendu i bazy danych. Jednak baza danych w takim projekcie nie jest wyłącznie schemą zapisaną w SQL. W rzeczywistości backend wpływa na ORM, migracje, modele, auth, strukturę danych wymaganą do uwierzytelniania, tabele techniczne i sposób testowania komunikacji z bazą. Dlatego, żeby całość pozostała w pełni natywna dla frameworków backendowych, będę traktował backend i bazę danych jako nierozerwalną całość - kosztem pewnego złamania DRY.
3. Baza danych wynika z wybranego backend-db stacka
   Nie wprowadzę pełnej macierzy dowolnego łączenia backendów i baz danych. W podstawowym zakresie pracy obsługiwane będą tylko stacki wskazane w specyfikacji: FastAPI + SQLite oraz Django + PostgreSQL. Dzięki temu każdy backend-db stack może pozostać natywny dla swojej technologii, a generator nie będzie wymuszał sztucznych kombinacji, które zwiększyłyby ilość pracy implementacyjnej, testowej i dokumentacyjnej.
4. Kontrakty zamiast jakichkolwiek adapterów
   Najprostszą drogą do agresywnego współdzielenia logiki między frameworkami byłoby wprowadzenie adapterów. Z perspektywy generowanego projektu takie adaptery są jednak absolutnie bezużyteczne. W tym projekcie nie dawałyby realnej wartości w wygenerowanej aplikacji, bo użytkownik otrzymałby dodatkową warstwę abstrakcji, której nie potrzebuje do dalszego rozwijania projektu. Dlatego, kosztem DRY i bardziej skomplikowanego kodu, świadomie rezygnuję z użycia adapterów pomiędzy różnymi frameworkami.
5. Template packi są jednostką rozszerzalności
   Nowa technologia, na przykład kolejny framework frontendowy lub kolejny backend-db stack powinny być dodawane jako nowy template pack, a nie warunki do core generatora. Core sprawdzi dostępne packi i na tej podstawie będzie walidował konfigurację.
6. Wygenerowany projekt jest samodzielny
   Po jednorazowym wygenerowaniu projekt nie potrzebuje generatora do dalszego funkcjonowania.
7. Idempotentność i staging
   Nieudana generacja nie może zostawić pozostałości w katalogu docelowym. Ponowne uruchomienie generatora dla tej samej konfiguracji powinno prowadzić do tej samej struktury projektu i nie może uszkadzać istniejącego wyniku. Każde uruchomienie generatora zaczyna od zera w nowym stagingu, a po błędzie generator sprząta cały run.

### 1.4 Relacja architektury do specyfikacji i kryteriów akceptacyjnych

Architektura jest projektowana z myślą o realizacji specyfikacji i spełnieniu wszystkich kryteriów akceptacyjnych. Ocena jej skuteczności będzie dokonywana właśnie na ich podstawie. Jeśli ta architektura zawiera jakiś element, to musi on odpowiadać na problem ze specyfikacji albo kryteriów. Architektura powinna być pod tym względem minimalna: nie rozwiązuje problemów innych niż te wskazane w specyfikacji i nie jest oceniana w inny sposób, niż to wynika z kryteriów akceptacyjnych.

- Plik ze specyfikacją: 2-specyfikacja.md
- Plik z kryteriami akceptacyjnymi: 3-kryteria-akceptacyjne.md

## 2 Słownik pojęć

### 2.1 Generator

Narzędzie CLI odpowiedzialne za utworzenie szkieletu aplikacji webowej na podstawie kreatora albo pliku konfiguracyjnego.

Generator nie jest częścią wygenerowanej aplikacji. Jego rola kończy się na przygotowaniu projektu, sprawdzeniu jego poprawności i zapisaniu wyniku w katalogu docelowym.

### 2.2 Wygenerowany projekt / Projekt

Szkielet aplikacji webowej utworzony przez generator.

Wygenerowany projekt zawiera frontend, backend, konfigurację Docker Compose, konfigurację środowiskową, testy oraz dokumentację. Po zakończeniu generacji projekt musi być możliwy do uruchomienia bez generatora.

### 2.3 Część projektu

Jedna z części wygenerowanego projektu: frontend, backend albo database. Każda część ma własny katalog oraz własne pliki .env i .env.example, a w konfiguracji jest kluczem w ports i envs. Część istnieje w projekcie, jeśli któryś z wybranych template packów deklaruje dla niej port.

Część projektu nie jest tym samym co usługa Docker Compose. Usługą jest też na przykład jednorazowa usługa migracji, która częścią projektu nie jest. Działająca usługa to kontener, a słowo moduł oznacza wyłącznie moduł kodu.

### 2.4 Konfiguracja

Zestaw danych wejściowych opisujących, jaki projekt ma zostać wygenerowany.

Konfiguracja może pochodzić z kreatora albo z pliku konfiguracyjnego. Zawiera między innymi nazwę projektu, katalog docelowy, wybrany frontend, wybrany backend-db stack, porty oraz zmienne środowiskowe. Po normalizacji konfiguracja jest uzupełniona o wartości domyślne i nazywa się znormalizowaną konfiguracją.

### 2.5 Kontrakt HTTP API

Zbiór wymagań określających sposób komunikacji pomiędzy frontendem i backendem.

Kontrakt HTTP API definiuje wymagane endpointy, format requestów, format response'ów, statusy HTTP oraz sposób użycia tokena JWT. Dzięki temu frontend nie musi znać konkretnej implementacji backendu i może komunikować się z każdym backendem spełniającym ten sam kontrakt.

### 2.6 Kontrakt danych backend-db

Zbiór minimalnych wymagań wobec backend-db stacka dotyczących danych wymaganych do działania aplikacji.

Kontrakt danych określa, że backend-db stack musi zapewnić minimalny model użytkownika pozwalający na jednoznaczną identyfikację użytkownika, rejestrację za pomocą emaila, logowanie za pomocą emaila, weryfikację hasła zapisanego jako hash oraz oznaczenie użytkownika jako aktywnego lub nieaktywnego.

Kontrakt danych nie wymaga identycznej fizycznej struktury tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez wybrany framework.

### 2.7 Template

Pojedynczy szablon pliku albo fragmentu pliku używany podczas generacji projektu.

Template może opisywać na przykład plik konfiguracyjny, plik źródłowy, test, fragment README.md albo fragment docker-compose.yml. Template nie powinien zawierać logiki wyboru technologii. Wybór technologii odbywa się wcześniej, na poziomie konfiguracji, rejestru template packów i planu generacji.

### 2.8 Template pack

Zestaw template'ów i manifestu odpowiadający za wygenerowanie konkretnej części projektu.

Template pack jest podstawową jednostką rozszerzalności generatora. Nowa technologia, na przykład nowy frontend albo nowy backend-db stack, powinna być dodawana jako nowy template pack, a nie jako dodatkowa logika warunkowa w core generatora.

### 2.9 Manifest template packa

Opis template packa zawierający informacje potrzebne generatorowi do jego użycia.

Manifest określa między innymi typ template packa, obsługiwaną technologię oraz inne, potrzebne informacje.

### 2.10 Rejestr template packów (template registry)

Rejestr dostępnych template packów, tworzony podczas procesu generacji.

Rejestr template packów pozwala generatorowi sprawdzić, jakie template packi są dostępne, które technologie obsługują i czy mogą zostać użyte dla wybranej konfiguracji. Dzięki temu core generatora nie musi znać szczegółów konkretnych frameworków.

### 2.11 Backend-db stack

Sprzężona para backendu i bazy danych traktowana jako jedna jednostka generacji.

Backend i baza danych są łączone w backend-db stack, ponieważ wybór backendu wpływa na ORM, migracje, modele, auth, strukturę danych wymaganą do uwierzytelniania, tabele techniczne oraz testowanie komunikacji z bazą. Przykładami backend-db stacków są FastAPI + SQLite oraz Django + PostgreSQL.

### 2.12 Core

Główna część generatora odpowiedzialna za obsługę procesu generacji.

Core odpowiada za wczytanie konfiguracji, walidację, wybór template packów, zbudowanie planu generacji, zarządzanie wykonaniem kroków pipeline'u, staging, finalizację i statystyki. Core nie powinien zawierać szczegółowej logiki konkretnych frameworków.

### 2.13 Pipeline

Pipeline to uporządkowana lista kroków generacji wykorzystywana przez core.

Pipeline nie jest samodzielnym silnikiem wykonawczym. Nie obsługuje błędów i nie przechodzi przez własne kroki sam. Te decyzje należą do core. Pipeline jedynie określa kolejność kroków i pozwala core przechodzić przez proces generacji w kontrolowany sposób.

### 2.14 Plan generacji (generation plan)

Plan technicznego wykonania generacji utworzony na podstawie konfiguracji i dobranych template packów. Jest zbiorem parametrów dla kroków pipeline'u.

Plan generacji określa, jakie template packi zostaną użyte, jakie pliki zostaną wygenerowane, jakie contributions zostaną dodane do plików składanych.

### 2.15 Contribution

Wkład template packa do pliku składanego, czyli pliku, który powstaje z template'ów częściowych kilku template packów.

Contribution jest używane tam, gdzie jeden plik powstaje z informacji dostarczanych przez wiele template packów. Przykładami takich plików są docker-compose.yml oraz README.md.

### 2.16 Staging

Katalog roboczy, w którym generator tworzy projekt przed zapisaniem go do katalogu docelowego.

Staging chroni katalog docelowy przed częściowo wygenerowanym lub uszkodzonym wynikiem. Projekt trafia do katalogu docelowego dopiero po poprawnym zakończeniu wymaganych kroków pipeline'u.

### 2.17 Katalog docelowy

Katalog podany przez użytkownika w polu project.output_dir, w którym powstaje katalog projektu. Musi istnieć, ale nie musi być pusty, a generator nie zmienia jego pozostałej zawartości.

### 2.18 Katalog projektu

Katalog o nazwie project.name wewnątrz katalogu docelowego, w którym powstaje projekt. Nie może istnieć albo musi być pusty, a wyjątek opisuje 10.3.

Katalog projektu zawiera wyłącznie poprawnie wygenerowany i zweryfikowany projekt. Nieudana generacja nie zostawia w nim częściowego wyniku.

### 2.19 Walidacja (validation)

Wszystkie sprawdzenia konfiguracji przed rozpoczęciem generacji. Pierwsza część odbywa się przy ładowaniu konfiguracji (6.4): struktura danych oraz istnienie i typ wskazanych template packów. Druga część odbywa się po normalizacji (6.6): porty, katalogi i zmienne środowiskowe. Błąd walidacji przerywa działanie, zanim generator zapisze jakikolwiek plik projektu.

### 2.20 Weryfikacja (verification)

Proces sprawdzania w stagingu, czy wygenerowany projekt działa: uruchomienie przez Docker Compose, testy kontraktu HTTP API, testy części projektu i test happy path. Szczegóły opisuje sekcja 15.

### 2.21 Idempotentność

Właściwość generatora oznaczająca, że ponowne uruchomienie dla tej samej konfiguracji nie prowadzi do niespójnego lub częściowo uszkodzonego projektu.

Idempotentność jest szczególnie ważna przy błędach generacji i ponownym uruchamianiu generatora dla tej samej konfiguracji.

### 2.22 Deterministyczność

Właściwość generatora oznaczająca, że ta sama konfiguracja powinna prowadzić do takiej samej struktury wygenerowanego projektu.

Deterministyczność dotyczy przede wszystkim struktury katalogów, wygenerowanych plików, dobranych template packów i planu generacji. Sekrety są losowane osobno dla każdego projektu, więc deterministyczność dotyczy struktury projektu, a nie ich wartości.

### 2.23 Artefakt

Katalog lub plik tworzony przez krok pipeline'u.

### 2.24 Sekret

Wymagana zmienna środowiskowa części projektu, zadeklarowana w manifeście template packa w required_envs. Jeśli użytkownik nie poda jej wartości, generator losuje ją osobno dla każdego projektu.

### 2.25 Run

Jedno uruchomienie generatora, od wczytania konfiguracji do finalizacji albo cleanupu. Każdy run ma własny katalog stagingu i własny projekt Docker Compose.

## 3 Ogólny model działania generatora

### 3.1 Przepływ i główne etapy działania

Generacja składa się z siedmiu etapów. Etapy 5-7 wykonuje pipeline jako ciąg kroków opisanych w 7.2.

1. Pozyskanie danych wejściowych.
   Generator zaczyna od otrzymania danych wejściowych. To jest jedynie deklaracja od użytkownika, co chce uzyskać:
   - nazwa projektu
   - katalog docelowy
   - frontend
   - backend-db stack
   - porty
   - zmienne środowiskowe

2. Normalizacja konfiguracji
   Generator przerabia dane wejściowe na spójną konfigurację wewnętrzną za pomocą wspólnego mechanizmu normalizacji danych wejściowych. Wartości zostają uporządkowane i uzupełnione, a wynikiem jest znormalizowana konfiguracja, na której podstawie powstanie projekt. Dzięki temu zarówno kreator, jak i plik konfiguracyjny mogą być interpretowane tak samo.

3. Walidacja
   Generator sprawdza, czy porty nie mają konfliktów, czy katalog docelowy istnieje i czy katalog projektu nie istnieje albo jest pusty. Istnienie i typ template packów sprawdza już ładowanie konfiguracji.

4. Stworzenie planu generacji
   Plan generacji jest zbiorem danych parametryzujących generację projektu. Zostanie on przekazany do pipeline'u. Planowanie wykrywa przy tym konflikty między packami, na przykład gdy dwa packi chcą wyrenderować ten sam plik. Odróżnia renderowanie pliku od składania go z kilku packów, informuje, jakie pliki składane zostaną stworzone.

5. Generowanie w katalogu roboczym
   Generator nie zaczyna od katalogu docelowego, ale robi staging. Na podstawie stałej listy kroków oraz planu generacji zostaje przeprowadzony cały proces - renderowanie template'ów, tworzenie struktury katalogów, zapis plików i przygotowanie konteneryzacji.

6. Weryfikacja
   Etap sprawdzenia, czy wygenerowany projekt rzeczywiście spełnia wymagania. Jest to główne odróżnienie tego generatora od prostego kopiowania template'ów. Poprawność projektu nie jest oceniana tym, że pliki powstały, tylko tym, że przechodzą wymagane testy.
   Weryfikacja uruchamia projekt przez Docker Compose, czeka, aż backend będzie gotowy (GET /health/ready), i uruchamia testy kontraktu HTTP API, testy wszystkich części projektu oraz test happy path.

7. Finalizacja
   Ostatni etap, przenoszący zweryfikowany projekt do katalogu docelowego. Jeśli weryfikacja nie zakończy się sukcesem, projekt nie zostaje przeniesiony do katalogu docelowego.

### 3.2 Tryb kreatora

Tryb interaktywnego CLI, zbierający dane wejściowe od użytkownika definiujące projekt.

### 3.3 Tryb pliku konfiguracyjnego

Tryb użycia jedynie nieinteraktywnego pliku konfiguracyjnego definiującego projekt.

## 4 Główne zasady architektoniczne

### 4.1 Frontend zależy wyłącznie od kontraktu HTTP API

Frontend nie wie nic o tym, jaki backend został wybrany. Dla frontendu istotne jest jedynie to, żeby backend wystawiał mu określone endpointy. Dzięki temu, rozszerzanie generatora o wsparcie dla dowolnych frontendów jest bardzo proste - ponieważ frontend pełni rolę warstwy prezentacji oraz klienta korzystającego z publicznego API backendu.

### 4.2 Backend i baza danych tworzą backend-db stack

Być może na papierze wygodne byłoby rozdzielenie backendu i bazy danych, żeby tworzyć dowolne kombinacje. Niestety, backend ma zbyt duży wpływ na sposób działania bazy danych:

- ORM
- migracje
- modele
- auth
- struktura danych wymagana do uwierzytelniania
- tabele techniczne
- testy backend-db

To wszystko sprawia, że obsługa takiej macierzy kombinacji szybko stałaby się nienatywna i pełna sztucznych warunków. Stąd decyzja o utrzymaniu backendu i bazy danych jako jednego backend-db stacka.

### 4.3 Baza danych wynikająca z backend-db stacka

Jest to świadome ograniczenie zakresu pracy. Użytkownik nie będzie mógł w podstawowej wersji dowolnie łączyć backendu z bazą danych. Jego decyzją będzie wybór jednego ze wspieranych backend-db stacków: FastAPI + SQLite albo Django + PostgreSQL. Dodanie większej liczby obsługiwanych stacków nie powinno wymagać zmiany założeń architektonicznych, ale zwiększyłoby ilość pracy implementacyjnej, testowej i dokumentacyjnej oraz spowodowałoby konieczność dodawania kolejnych stacków jeden po drugim. Dlatego podstawowa wersja pracy zawiera tylko stacki wskazane w specyfikacji.

### 4.4 Kontrakty zamiast adapterów

Ta zasada chroni projekt przed sztuczną warstwą abstrakcji, jaką byłby dowolny adapter. Nie chcę, żeby projekt miał dodatkowe adaptery tylko dlatego, że generator obsłuży inne kombinacje. Dzięki temu spójność zostanie osiągnięta przez kontrakty:

- Frontend jest kompatybilny z backendem, bo spełniają kontrakt API,
- Backend-db stack jest zgodny z wymaganiami projektu, bo spełnia kontrakt danych.

Dzięki temu nie trzeba będzie dodawać sztucznych adapterów, bo kontrakty zapewnią spójność, a template packi zachowają natywność wygenerowanego kodu.

### 4.5 Natywność template packów

Template pack będzie generował kod, który jest naturalny dla danej technologii. Django nie zostanie wciśnięte w typową strukturę FastAPI, a Nuxt nie będzie udawać Reacta. Dlatego kluczowe będzie dokładne zapoznanie się ze wzorcami standardowymi dla obsługiwanych technologii, a następnie utworzenie każdego template packa zgodnie z nimi. Przykład konwencji:

- Django -> Django ORM, migracje Django, struktura Django
- FastAPI -> struktura FastAPI, osobna konfiguracja aplikacji, osobne modele/schemy
- Nuxt -> routing oparty na plikach, struktura typowa dla Nuxta

Jeśli wspólne będą jedynie wymagania, a nie struktura kodu, osiągniemy naturalny projekt, pozbawiony złych nawyków lub wymuszeń związanych z innymi frameworkami.

### 4.6 Kontrolowane powtórzenia zamiast sztucznych abstrakcji

W zwykłym projekcie często dąży się do DRY. W wypadku generatora zbyt agresywne DRY mogłoby jednak sprawić, że ucierpią na tym generowane projekty. Współdzielenie jednej abstrakcji między różnymi frameworkami skończyłoby się strukturą nienaturalną dla żadnego z nich. Z tego powodu akceptuję pewne powtórzenia, jeśli są konieczne, żeby:

- template pack pozostał natywny
- wygenerowany kod pozostał czytelny
- framework działał zgodnie z typowymi dla siebie konwencjami
- nowa technologia nie wymagała modyfikowania starej

Dlatego wygenerowane projekty powinny być możliwie DRY, ale sam generator może świadomie zawierać kontrolowane powtórzenia w template packach.

### 4.7 Wygenerowany projekt nie zależy runtime'owo od generatora

Generator jest jedynie narzędziem do tworzenia projektu, a nie jego częścią. Projekt po skopiowaniu do katalogu docelowego ma funkcjonować bez generatora. Wygenerowany projekt nie powinien importować bibliotek generatora ani wymagać go do uruchamiania, testowania lub dalszego rozwijania.

## 5 Podział systemu na główne części

### 5.1 Core

Core jest głównym modułem sterującym generatora. Core nie może znać szczegółów frameworków, z jakich korzysta. Musi on orkiestrować cały proces generacji:

- uruchomienie CLI
- wczytanie danych
- normalizacja konfiguracji
- walidacja
- planowanie
- zarządzanie wykonaniem kroków pipeline'u
- obsługa błędów
- przekazanie wyniku do outputu
- zebranie statystyk

Dzięki temu, w przypadku rozszerzania o kolejne technologie, core nie powinien wymagać istotnych modyfikacji.

### 5.2 Pipeline

Zarządzany przez core iterowalny proces, przechodzący przez renderowanie, weryfikację i finalizację. Pipeline przechodzi przez kroki wyłącznie w przód, a po błędzie core sprząta cały run.

### 5.3 Template packs

Część systemu, która dostarcza kod i konfigurację dla konkretnych technologii. Template packi znają szczegóły frameworków, mieści się w nich docelowa struktura generowanego kodu.
Template packi powinny być możliwie niezależne od siebie i komunikować się przez kontrakty oraz contributions. Jeśli autor chce rozszerzyć generator o obsługę kolejnej technologii, po prostu dodaje kolejny template pack. To tam mieści się cały kod, konfiguracja, obsługa kontraktów. Dzięki temu, wystarczy w zasadzie dobrze znać wybrany framework, żeby móc utworzyć dla niego template pack.

Istnieją dwa typy template packów: frontend i backend-db. Template pack zawiera template'y całościowe, z których powstają pliki całościowe, oraz template'y częściowe (contributions), z których powstają pliki składane.

### 5.4 Planowanie

Część odpowiedzialna za przetłumaczenie konfiguracji na plan generacji. Na tym etapie konfiguracja zostaje zamieniona na zestaw template packów, contributions i danych potrzebnych do renderowania. Dzięki niemu proces jest przewidywalny i deterministyczny oraz gwarantuje poprawny plan.

### 5.5 Renderowanie

Proces zmieniający template'y wybrane w planie generacji na pliki w katalogu roboczym. Renderer kopiuje pliki całościowe i składa pliki składane z contributions.

### 5.6 Output

Output odpowiada za operacje na plikach i katalogach poza samym renderowaniem template'ów. Pilnuje, żeby w katalogu docelowym nie znalazł się uszkodzony wynik.

Zadania outputu:

- utworzenie pustego katalogu stagingu dla runa
- zapis plików .env z wartościami ze znormalizowanej konfiguracji (14.5)
- przeniesienie zweryfikowanego projektu do katalogu projektu (9.4)
- wykonanie cleanupu runa na polecenie core (sekcja 8)

### 5.7 Weryfikacja

Weryfikacja sprawdza, czy projekt w stagingu działa poprawnie. Wygenerowany projekt, zanim trafi do katalogu docelowego, jest dokładnie sprawdzany w katalogu stagingu. Dzięki temu nie wprowadzamy niedziałającego projektu do katalogu docelowego. Weryfikacja jest wykonywana jako jeden lub kilka kroków pipeline'u zarządzanego przez core.

### 5.8 Statystyki

Część odpowiedzialna za mierzenie i raportowanie przebiegu generacji. Pozwala porównywać czas trwania etapów oraz czas generacji różnych kombinacji technologicznych. Listę zbieranych danych opisuje sekcja 16.

## 6 Core generatora

### 6.1 Odpowiedzialność core

Core odpowiada za przebieg całej generacji.
Core orkiestruje:

- uruchomienie generatora
- obsługę trybu kreatora i configu
- wczytanie danych wejściowych
- normalizację konfiguracji
- walidację konfiguracji
- budowanie planu generacji
- zarządzanie wykonaniem kroków pipeline'u
- obsługę błędów
- przekazanie wyniku do outputu
- zebranie statystyk

### 6.2 Czego core nie powinien zawierać

Core nie może wiedzieć, co dokładnie orkiestruje, w szczególności nie powinien znać:

- struktury katalogów frameworka
- nazw plików frameworka
- konkretnych zależności technologii
- szczegółów migracji
- konkretnego frameworka testowego w wygenerowanym projekcie

To wszystko musi pozostać w template packach i ich manifestach.

### 6.3 Obsługa CLI

CLI jest wejściem użytkownika do generatora. Jest podmodułem core'a i jego zadaniem jest jedynie pozyskanie ustrukturyzowanych danych wejściowych i przekazanie ich dalej.
CLI obsługuje dwa tryby wejścia:

- tryb kreatora
- tryb pliku konfiguracyjnego

Po zakończeniu kreatora, przed normalizacją, CLI zapisuje odpowiedzi jako plik konfiguracyjny `<project.name>.yaml` w bieżącym katalogu i wypisuje jego ścieżkę. Jeśli taki plik już istnieje, CLI pyta, czy go nadpisać.

CLI wyświetla użytkownikowi:

- postęp generacji
- błędy w procesie generacji
- statystyki z procesu generacji

### 6.4 Ładowanie konfiguracji

Kiedy CLI już przygotuje dane wejściowe, przekazuje je do core'a. Dane są sprawdzane pod kątem poprawności struktury i syntaktyki. Sprawdzane jest też, czy template packi wskazane jako frontend i backend istnieją w rejestrze template packów i mają właściwy typ. Kreator robi to przy wyborze packa, a tryb pliku konfiguracyjnego zaraz po wczytaniu pliku. To pierwsza część walidacji. Następnie dane są przekazywane do modułu normalizacji konfiguracji.

### 6.5 Normalizacja konfiguracji

Tutaj konfiguracja zostaje uporządkowana i znormalizowana. Wynikiem normalizacji jest znormalizowana konfiguracja: uporządkowana, uzupełniona o dane domyślne i poprawna semantycznie. Poprawność semantyczna oznacza tutaj spójne znaczenie danych, a nie potwierdzenie, że dana technologia lub kombinacja jest obsługiwana przez generator.
Normalizacja obejmuje:

- uzupełnienie domyślnych portów
- wylosowanie brakujących sekretów wymaganych przez template packi
- pominięcie z ostrzeżeniem portów i zmiennych środowiskowych, których nie deklarują wybrane template packi

### 6.6 Walidacja konfiguracji

Po normalizacji druga część walidacji sprawdza, czy z tej konfiguracji można bezpiecznie wygenerować projekt.
Walidacja obejmuje sprawdzenie:

- czy porty nie mają konfliktów
- czy katalog docelowy istnieje i pozwala na zapis, a katalog projektu nie istnieje albo jest pusty

### 6.7 Budowanie planu generacji

Plan generacji przekłada język konfiguracji na docelowy plan wykonania, używający już konkretnych zasobów.
Plan określa:

- wybrane template packi
- pliki składane z contributions
- dane projektu

Przy budowaniu planu planowanie wykrywa konflikty między template packami: dwa packi dostarczają plik całościowy o tej samej ścieżce albo jeden dostarcza plik całościowy, a drugi contribution do tego samego pliku. Konflikt przerywa działanie, zanim generator zapisze jakikolwiek plik projektu.

### 6.8 Pipeline jako podmoduł core

Pipeline jest stałą listą kroków wykonywanych po kolei. Plan generacji nie zmienia tej listy, tylko dostarcza krokom parametry. Decyzja, czy przejść dalej, czy przerwać generację, należy do core.

### 6.9 Zarządzanie wykonaniem kroków pipeline'u

Pipeline wykonuje kroki z parametrami z planu generacji. Core zarządza przebiegiem wykonania, odbiera wynik kroku i decyduje, czy można przejść do kolejnego kroku.

Krok jest uznawany za ukończony dopiero po pełnym sukcesie. W przeciwnym wypadku core przerywa generację i uruchamia cleanup.

### 6.10 Obsługa błędów i przerwania generacji

Jeśli wystąpi błąd, pipeline przekazuje informację o błędzie do core. Core zatrzymuje przechodzenie do kolejnych kroków, przekazuje informację o błędzie do statystyk i uruchamia cleanup całego runa. Tak samo core postępuje przy przerwaniu generacji przez użytkownika.

### 6.11 Zbieranie statystyk

Core mierzy czas etapów i kroków pipeline'u i przekazuje te dane oraz informację o błędzie do statystyk. Listę zbieranych danych opisuje sekcja 16.

## 7 Pipeline zarządzany przez core

### 7.1 Rola pipeline'u w architekturze

Pipeline jest stałą listą kroków wykonywanych po kolei. Kroki dostają parametry z planu generacji. Decyzja, czy przejść dalej, podejmowana jest przez core.

Odpowiedzialności pipeline'u:

- definicja listy kroków
- wykonywanie poszczególnych kroków
- zwracanie wyniku kroku do core

Pipeline wykonuje też krok finalizacji, ale decyzja, czy do niego dojść, należy do core.

### 7.2 Pipeline jako uporządkowana lista kroków

Lista kroków jest stała. W zależności od wybranych template packów niektóre kroki dostają z planu generacji inne parametry.

Kroki pipeline'u:

1. Utworzenie katalogu stagingu i zapis śladu runa.
2. Skopiowanie plików całościowych z template packów.
3. Złożenie plików składanych z contributions.
4. Zapis plików .env z wartościami ze znormalizowanej konfiguracji.
5. Zbudowanie obrazów przez Docker Compose.
6. Uruchomienie projektu przez Docker Compose.
7. Sprawdzenie, czy jednorazowe usługi inicjalizujące zakończyły się kodem 0, a backend osiągnął stan healthy.
8. Uruchomienie testów kontraktu HTTP API na działającym backendzie.
9. Uruchomienie testów każdej części projektu.
10. Uruchomienie testu happy path.
11. Zatrzymanie projektu i usunięcie jego zasobów Dockera.
12. Kopia projektu do katalogu tymczasowego w katalogu docelowym.
13. Zmiana nazwy kopii na katalog projektu.
14. Usunięcie katalogu stagingu.

Generator nie instaluje zależności na komputerze użytkownika. Zależności instalowane są w ramach Docker builda, a pliki blokujące wersje, np. package-lock.json, są częścią template packa.

### 7.3 Granice odpowiedzialności pipeline'u

Pipeline jest narzędziem pomocniczym dla core. Pipeline nie podejmuje decyzji o przerwaniu procesu ani o tym, czy dojść do finalizacji.

Jeśli pojawi się błąd, pipeline przekazuje go do core. Core przerywa generację, uruchamia cleanup i zwraca błąd użytkownikowi.

### 7.4 Krok pipeline'u

Krok pipeline'u to pojedyncza operacja zdefiniowana w liście kroków.

Krok może tworzyć artefakty oraz efekty uboczne. Artefaktami są na przykład pliki i katalogi. Efektami ubocznymi mogą być na przykład uruchomione kontenery Docker, wolumeny, sieci albo dane utworzone podczas testów.

Krok powinien mieć określone:

- co wykonuje
- po czym poznać, że zakończył się sukcesem
- jak posprzątać po błędzie, jeśli zostawia coś poza stagingiem i projektem Docker Compose runa

### 7.5 Kolejność kroków pipeline'u

Kroki wykonywane są zawsze w tej samej kolejności, zdefiniowanej w pipelinie.

Podstawowy model pipeline'u jest liniowy. Warunkowe różnice, na przykład obecność osobnego kontenera database dla Django + PostgreSQL i jego brak dla FastAPI + SQLite, powinny wynikać z planu generacji oraz manifestów template packów.

### 7.6 Relacja pipeline'u z core

Pipeline to uporządkowany mechanizm kroków, z którego korzysta core.

Core:

- uruchamia pipeline z planem generacji
- uruchamia kolejne kroki
- obsługuje błędy
- decyduje o przerwaniu procesu i cleanupie

### 7.7 Relacja pipeline'u z planem generacji

Kroki pipeline'u są stałe, a plan generacji dostarcza im parametry: jakie template packi, pliki, contributions i testy weryfikacji są wymagane dla danej konfiguracji.

Dzięki temu pipeline nie musi zawierać logiki konkretnych technologii.

## 8 Cleanup

### 8.1 Rola cleanupu

Cleanup sprawia, że nieudana albo przerwana generacja nie zostawia śladów: częściowego projektu w katalogu docelowym, plików w stagingu ani zasobów Dockera. Cleanup obejmuje zawsze cały run, a nie pojedynczy krok.

### 8.2 Zakres cleanupu

Cleanup runa:

- zatrzymuje i usuwa kontenery, sieci, wolumeny i obrazy projektu Docker Compose runa
- usuwa katalog stagingu runa
- usuwa kopię tymczasową z katalogu docelowego, jeśli błąd wystąpił podczas finalizacji

### 8.3 Projekt Docker Compose runa

Weryfikacja uruchamia projekt w osobnym projekcie Docker Compose o nazwie unikalnej dla runa. Dzięki temu wszystkie efekty uboczne Dockera da się usunąć bez wiedzy o tym, który krok je utworzył. Obrazy budowane przez template packi nie mogą mieć stałych nazw, bo stała nazwa koliduje między projektami i wypada poza cleanup runa.

### 8.4 Ślad runa

Na początku runa generator zapisuje w stagingu dane potrzebne do cleanupu: nazwę projektu Docker Compose runa i ścieżkę kopii tymczasowej. Jeśli proces zostanie zabity, cleanup się nie wykona. Wtedy kolejne uruchomienie generatora najpierw sprząta po poprzednich runach na podstawie ich śladów, a dopiero potem zaczyna nowy run.

## 9 Staging i output

### 9.1 Rola stagingu

Staging zapewnia, że katalog docelowy nie zostaje zaśmiecony niedziałającym projektem. Staging znajduje się w katalogu TEMP generatora. Każdy run dostaje własny, pusty katalog stagingu, który po zakończeniu runa, udanym albo nie, zostaje usunięty. Gwarantuje to, że na dysku nie pozostanie żaden niesprawdzony, niedziałający efekt generacji.

### 9.2 Katalog roboczy generacji

Katalogiem roboczym runa jest jego podkatalog w katalogu TEMP generatora.

### 9.3 Katalog docelowy i katalog projektu

Katalog docelowy podaje użytkownik w polu project.output_dir. Katalog projektu powstaje w nim i ma nazwę project.name.

### 9.4 Finalizacja poprawnej generacji

Po udanej generacji i zakończeniu weryfikacji projekt zostaje skopiowany do katalogu tymczasowego w katalogu docelowym, a następnie przemianowany na katalog projektu. Kopia trafia do katalogu docelowego, a nie do stagingu, bo zmiana nazwy jest atomowa tylko w obrębie jednego dysku. Dzięki temu przerwana kopia nie zostawia częściowego projektu w katalogu projektu. Jeśli użytkownik potwierdził użycie istniejącego katalogu projektu, jego zawartość jest usuwana dopiero w tym momencie, tuż przed zmianą nazwy.

## 10 Konfiguracja wejściowa

### 10.1 Zestaw danych wejściowych

Dane wejściowe zawsze będą zawierały:

- nazwa projektu
- katalog docelowy
- frontend
- backend-db stack
- porty do wykorzystania
- zmienne środowiskowe

### 10.2 Kreator a plik konfiguracyjny

Oba zakończą się utworzeniem identycznej konfiguracji. Różnice są wyłącznie w zachowaniu.

Kreator sprawdza dane po każdym pytaniu i od razu daje użytkownikowi możliwość ich poprawienia.
Plik konfiguracyjny jest sprawdzany jako całość. Niepoprawny plik kończy się rzuceniem błędu z informacją, co należy zmienić.
W trybie pliku konfiguracyjnego sytuacje, które kreator rozwiązuje potwierdzeniem, czyli niepusty katalog projektu i port zajęty przez inny proces, kończą się błędem, chyba że generator uruchomiono z flagą `--force`.

### 10.3 Konfiguracja projektu

Bezwzględna ścieżka katalogu docelowego oraz nazwa projektu. Projekt powstaje w katalogu projektu o nazwie project.name wewnątrz katalogu docelowego.

Katalog docelowy musi istnieć i umożliwiać zapis i odczyt plików, ale nie musi być pusty. Katalog projektu nie może istnieć albo musi być pusty. Jeśli istnieje i nie jest pusty, użytkownik musi potwierdzić jego użycie w kreatorze albo uruchomić generator z flagą `--force` - wtedy jego zawartość zostanie usunięta podczas finalizacji, po pozytywnej weryfikacji. Czyszczenie nigdy nie obejmuje pozostałej zawartości katalogu docelowego.

### 10.4 Konfiguracja frontendu

Wybór template packa z dostępnych frontendów. Plik konfiguracyjny jest walidowany pod kątem dostępności, kreator pozwala wybrać tylko spośród dostępnych.

### 10.5 Konfiguracja backend-db stacka

Wybór template packa z dostępnych backendów. Plik konfiguracyjny jest walidowany pod kątem dostępności, kreator pozwala wybrać tylko spośród dostępnych.

### 10.6 Konfiguracja portów

Konflikt portów oznacza, że dwie części projektu mają ten sam port hosta. Port zajęty oznacza, że port hosta jest używany przez inny proces na komputerze użytkownika. Plik konfiguracyjny może podać port dla każdej części projektu. Null albo brak wpisu oznacza port domyślny z manifestu template packa. Część projektu istnieje w generowanym projekcie, jeśli któryś z wybranych template packów deklaruje dla niej port. Część, która nie istnieje, nie dostaje portu, a podany dla niej port jest pomijany z ostrzeżeniem. Kreator od razu sprawdza, czy port nie ma konfliktu i czy nie jest zajęty. Nie można użyć portu z konfliktem, ale port zajęty jest przepuszczany z ostrzeżeniem wymagającym potwierdzenia.

### 10.7 Konfiguracja środowiskowa

Sekrety można tutaj podać, a brakujące generator losuje osobno dla każdego projektu. Każdy template pack może oczekiwać zmiennych środowiskowych. Wartości są podawane osobno dla każdej części projektu i trafiają do jej własnego pliku .env. Zmienne, których nie wymaga żaden z wybranych template packów, są pomijane z ostrzeżeniem. Każda istniejąca część projektu ma w znormalizowanej konfiguracji swoją sekcję zmiennych, nawet pustą, a część, która nie istnieje, nie ma jej wcale.

### 10.8 Wartości domyślne

Frontend, backend-db stack, katalog docelowy i nazwa projektu muszą być podane. Domyślny port to port z manifestu template packa, a brakujące sekrety są losowane.

## 11 Plan generacji

### 11.1 Rola planu generacji

Plan generacji to dane, które parametryzują stałą listę kroków pipeline'u. Powstaje na podstawie znormalizowanej konfiguracji i manifestów wybranych template packów.

### 11.2 Wzór planu generacji

- katalog docelowy
- nazwa projektu
- frontend template pack
- backend-db stack template pack
- lista plików składanych z contributions

### 11.3 Utworzenie planu generacji

Plan generacji powstaje w etapie planowania, po walidacji konfiguracji. Pipeline nie zmienia planu, tylko odczytuje z niego parametry dla swoich kroków.

## 12 Model kontraktów

### 12.1 Rola kontraktów w architekturze

Kontrakty pilnują, żeby poszczególne części projektu były ze sobą kompatybilne i komunikowały się ze sobą. Wymuszają jeden określony sposób komunikacji.

### 12.2 Kontrakt HTTP API

Lista endpointów, których oczekuje frontend i które musi zagwarantować backend. Specyfikacja, jak każdy z nich ma wyglądać i zachowywać się. Specyfikacja błędów, jakich można od nich oczekiwać.

### 12.3 Kontrakt danych backend-db

Minimalne wymagania funkcjonalne i strukturalne wobec danych wymaganych do działania mechanizmu uwierzytelniania. Kontrakt danych nie wymusza identycznej fizycznej struktury tabel, ale wymaga, aby backend-db stack zapewniał możliwość identyfikacji użytkownika, rejestracji, logowania, weryfikacji hasła jako hasha oraz oznaczenia użytkownika jako aktywnego albo nieaktywnego.

### 12.4 Zgodność template packów z kontraktami

Każdy dodany template pack musi spełniać kontrakty przypisane do jego typu, inaczej nie będzie kompatybilny z innymi. Frontend musi być zgodny z kontraktem HTTP API, a backend-db stack z kontraktem HTTP API oraz kontraktem danych. Ponieważ kontrakty wynikają z typu template packa, nie są deklarowane w manifeście.

### 12.5 Testowanie zgodności z kontraktami

Zgodność backendu z kontraktem HTTP API sprawdzają wspólne testy kontraktu w katalogu contracts generatora. Testy wysyłają requesty do działającego backendu i porównują statusy, kształty odpowiedzi i wartości detail ze specyfikacją, więc nie zależą od technologii backendu. Generator uruchamia je w weryfikacji każdego projektu. Przypadków, których nie da się wywołać przez samo API, np. logowania nieaktywnego użytkownika, pilnują testy integracyjne backendu.

Każdy frontend dostarcza test happy path, który na działającym projekcie rejestruje użytkownika, loguje go i pobiera jego dane, korzystając z tego samego klienta HTTP co strony aplikacji. Test nie zależy od wybranego backendu, więc ten sam test sprawdza każdy backend-db stack zgodny z kontraktem HTTP API. Jeśli test nie przejdzie, kontrakt nie jest spełniony.

## 13 Template'y i template packi

### 13.1 Rola template'ów

Template to pojedynczy plik, będący częścią template packa. Template całościowy staje się plikiem całościowym projektu, a template częściowy (contribution) staje się fragmentem pliku składanego. Renderowanie template'u całościowego sprowadza się do jego skopiowania w odpowiednie miejsce, a częściowego do doklejenia go do pliku składanego.

### 13.2 Rola template packów

Template pack składa się z template'ów całościowych, template'ów częściowych oraz manifestu.
Template'y całościowe są po prostu katalogiem do skopiowania.
Template'y częściowe zawierają treść oraz informację, do którego pliku składanego należą.
Manifest określa typ template packa i jego wersję.

### 13.3 Template pack jako jednostka rozszerzalności

Kiedy core zostanie ukończony, rozszerzanie generatora o kolejne wspierane frameworki będzie możliwe poprzez dodanie kolejnego template packa. Celem jest, aby nowa technologia nie wymagała zmiany czegokolwiek i jedynie wymagała dodanie nowego template packa.

### 13.4 Manifest template packa

Manifest zawiera potrzebne informacje o template packu. To na podstawie manifestu zostaje dopasowany odpowiedni template pack.

Dane zawarte w manifeście (\* oznacza daną opcjonalną):

- Nazwa wyświetlana (name). Identyfikatorem template packa jest nazwa jego katalogu
- Typ (type): frontend albo backend-db
- Wersja template packa (version)
- Nazwa i wersja frameworka (framework)
- Nazwa i wersja języka programowania (language)
- \*Silnik i wersja bazy danych (database)
- Poziom stabilności (stability): alpha, beta albo stable
- Domyślny port hosta dla każdej części projektu (ports)
- Lista sekretów dla każdej części projektu (required_envs)
- Lista plików składanych, do których template pack dostarcza contributions (contributions)

Domyślny port oznacza, że template pack dostarcza daną część projektu. Sekrety wymagane dla części projektu, dla której żaden z wybranych template packów nie deklaruje portu, są pomijane.

Sekrety wymagane przez kilka template packów w tej samej części projektu są łączone i mają jedną wspólną wartość.

Sposób uruchomienia testów nie jest częścią manifestu. Każdy template pack musi dostarczać makefile z targetem `test`, który uruchamia jego testy. Template pack frontendu dostarcza też target `happy-path`, który uruchamia test happy path na działającym projekcie.

Zależności również nie są częścią manifestu. Template pack deklaruje je w natywnym pliku zależności swojej technologii, na przykład pyproject.toml albo package.json. Zależności między template packami wynikają z ich typów.

Generowane pliki nie są wymieniane w manifeście. Wynikają z zawartości katalogu template'ów całościowych template packa.

### 13.5 Jakość template packa

Template pack powinien być bazą modułu/frameworka/biblioteki napisanego zgodnie z najlepszymi, standardowymi dla niego praktykami. Powinien być stworzony w sposób natywny i łatwo rozszerzalny dla użytkownika.

### 13.6 Typy template packów

#### 13.6.1 Frontend pack

Zawiera framework z frontendem. Jest wymagany do każdego projektu.

#### 13.6.2 Backend-db pack

Zawiera framework z backend-db stackiem. Jest wymagany do każdego projektu.

### 13.7 Wybór template packów

#### 13.7.1 Rejestr template packów

Rejestr jest tworzony podczas każdego wykonania programu. Wszystkie dostępne template packi znajdujące się w katalogu template_packs są sprawdzane, a dane pobierane z ich manifestów. Na tej podstawie następuje kategoryzacja.

Identyfikatorem template packa jest nazwa jego katalogu. Katalog bez pliku manifest.yaml jest pomijany z ostrzeżeniem. Niepoprawny manifest przerywa działanie generatora błędem, który wskazuje, co należy poprawić.

#### 13.7.2 Dobór template packów

Projekt powstaje zawsze z dwóch template packów: jednego frontendu i jednego backend-db stacka. Każdy z nich dostarcza Dockerfile swojej części projektu i swoją contribution do docker-compose.yml.

#### 13.7.3 Wykrywanie niewspieranych konfiguracji

Każda para template packów frontendu i backend-db stacka z rejestru tworzy wspieraną kombinację, bo łączy je wyłącznie kontrakt HTTP API. Niewspierana konfiguracja to taka, która wskazuje template pack spoza rejestru albo template pack złego typu. Odrzuca ją ładowanie konfiguracji (6.4).

## 14 Renderowanie

### 14.1 Rola renderowania

Renderowanie to proces faktycznej generacji zawartości projektu. Pliki są kopiowane i składane w odpowiedni sposób, a wynikiem jest gotowy projekt.

### 14.2 Renderowanie plików całościowych

Pliki całościowe są bardzo proste do wyrenderowania. Wystarczy skopiować template'y całościowe do odpowiedniego katalogu.

### 14.3 Renderowanie plików składanych

Pliki składane tworzone są z template'ów częściowych. Jeden z kroków pipeline'u tworzy wszystkie pliki składane i ich wspólny początek, a następnie dokleja contributions kolejnych template packów.

Pliki są zawsze składane w tej samej kolejności:

- Wstęp
- Frontend
- Backend-db stack
- Zakończenie

Jeśli któryś z template packów nie dostarcza contribution do pliku, kolejność i tak pozostaje zachowana - po prostu bez niego.

Dla plików strukturalnych, takich jak docker-compose.yml, contributions są składane w ramach nazwanych sekcji, na przykład services, volumes i networks. W obrębie sekcji obowiązuje stała kolejność składania.

### 14.4 Ograniczenie logiki w rendererze

Renderer jedynie kopiuje pliki lub skleja zawartość plików według prostego schematu. Dzięki temu nie ma ciężkiej logiki i jest stosunkowo mało podatny na błędy, a także niezależny od tego, co renderuje.

### 14.5 Wartości z konfiguracji

Renderer nie podstawia w template'ach żadnych wartości. Wartości ze znormalizowanej konfiguracji trafiają do projektu wyłącznie przez pliki .env, które generator zapisuje osobnym krokiem pipeline'u. Każda część projektu dostaje własny .env ze swoimi zmiennymi i sekretami oraz .env.example z tymi samymi kluczami bez wartości sekretów. Główny .env zawiera porty części projektu w postaci `<CZĘŚĆ>_PORT`, np. `BACKEND_PORT`, które docker-compose.yml odczytuje przez interpolację zmiennych. Nazwa projektu Docker Compose wynika z nazwy katalogu projektu.

Dzięki temu template pack pozostaje działającą aplikacją, którą da się uruchomić i przetestować bez generatora.

## 15 Weryfikacja

Weryfikacja sprawdza w stagingu, czy wygenerowany projekt działa, zanim trafi do katalogu docelowego. Obejmuje kroki 5-11 pipeline'u z 7.2:

- zbudowanie i uruchomienie projektu w projekcie Docker Compose runa
- sprawdzenie, czy jednorazowe usługi inicjalizujące zakończyły się kodem 0, a backend osiągnął stan healthy na podstawie GET /health/ready
- uruchomienie testów kontraktu HTTP API z katalogu contracts generatora
- uruchomienie testów każdej części projektu przez make test
- uruchomienie testu happy path
- zatrzymanie projektu i usunięcie jego zasobów Dockera

Po weryfikacji pipeline wykonuje jeszcze finalizację.

## 16 Statystyki

Statystyki pozwolą podsumować i porównać różne template packi. CLI pokazuje je użytkownikowi po zakończeniu generacji. Zbierane są:

- czas całej generacji
- czas poszczególnych etapów i kroków pipeline'u
- wybrana kombinacja technologiczna
- liczba wygenerowanych plików
- liczba użytych template packów
- status weryfikacji
- etap albo krok pipeline'u, na którym wystąpił błąd, i treść błędu

## 17 Struktura katalogów generatora

```text
|--/generator
|  |--/cli
|  |--/common
|  |--/configuration
|  |--/core
|  |--/registry
|  |--/settings
|  |--/verification
|--/template_packs
|--/contracts
|--/docs
|--/docker
|--/TEMP
|--/log
|--main.py
|--makefile
|--pyproject.toml
|--docker-compose.yml
|--.env
|--.env.example
|--README.md
|--.gitignore
|--.dockerignore
```

## 18 Struktura wygenerowanego projektu

```text
|--/docs
|--/frontend
|--/backend
|--/database *opcjonalny
|--.env
|--.env.example
|--README.md
|--docker-compose.yml
|--.gitignore
|--.dockerignore
```

Każda część projektu ma własne pliki .env i .env.example, a główny .env zawiera porty części projektu dla docker-compose.yml.

## 19 Powiązanie architektury z kryteriami akceptacyjnymi

### 19.1 Kryteria generatora

Za spełnienie kryteriów dotyczących działania generatora odpowiada przede wszystkim core.

Core obsługuje uruchomienie generatora jako narzędzia CLI, wczytanie danych wejściowych, normalizację konfiguracji, walidację, przygotowanie planu generacji, wykonanie pipeline'u oraz zebranie statystyk.

Tryb kreatora oraz tryb pliku konfiguracyjnego są sprowadzane do tej samej znormalizowanej konfiguracji. Dzięki temu dalsze etapy generatora działają tak samo niezależnie od źródła danych wejściowych.

Walidacja konfiguracji przed rozpoczęciem generacji pozwala spełnić kryteria dotyczące wykrywania błędnych danych wejściowych, nieznanych template packów, konfliktów portów, niepoprawnego katalogu docelowego oraz niepustego katalogu projektu.

### 19.2 Kryteria wspieranych kombinacji

Za spełnienie kryteriów dotyczących wspieranych kombinacji technologicznych odpowiadają rejestr template packów, manifesty template packów oraz plan generacji.

Każda wspierana technologia jest dostarczana przez odpowiedni template pack. Generator nie wybiera frameworków przez warunki zaszyte w core, tylko przez informacje zawarte w manifestach. Dzięki temu możliwe jest sprawdzenie, czy dla wskazanej konfiguracji istnieje komplet wymaganych template packów.

W podstawowym zakresie projektu obsługiwane są kombinacje wynikające ze specyfikacji:

- Nuxt + FastAPI + SQLite
- Nuxt + Django + PostgreSQL

Konfiguracja z nieznanym template packiem albo packiem złego typu jest odrzucana przy ładowaniu konfiguracji, zanim generator rozpocznie zapis plików.

### 19.3 Kryteria wygenerowanego projektu

Za spełnienie kryteriów dotyczących wygenerowanego projektu odpowiadają template packi, renderowanie, output oraz weryfikacja.

Template packi dostarczają pliki źródłowe, konfigurację środowiskową, pliki Docker, testy oraz dokumentację. Renderowanie odpowiada za fizyczne utworzenie struktury projektu w katalogu roboczym. Output odpowiada za przeniesienie zweryfikowanego projektu do katalogu docelowego.

Wygenerowany projekt musi zawierać co najmniej:

- frontend
- backend
- docker-compose.yml
- .env i .env.example w katalogu głównym i w każdej części projektu
- README.md
- testy

Projekt po wygenerowaniu nie może zależeć runtime'owo od generatora.

### 19.4 Kryteria kontraktów

Za spełnienie kryteriów dotyczących kontraktów odpowiadają kontrakt HTTP API, kontrakt danych backend-db oraz weryfikacja.

Kontrakt HTTP API zapewnia spójność komunikacji między frontendem i backendem. Każdy frontend korzysta z tych samych endpointów, a każdy backend musi te endpointy udostępnić zgodnie ze specyfikacją.

Kontrakt danych backend-db określa minimalne wymagania wobec danych potrzebnych do działania mechanizmu rejestracji, logowania i pobierania aktualnego użytkownika. Kontrakt danych nie wymusza identycznej fizycznej struktury tabel we wszystkich backendach, ale wymaga, aby każdy backend-db stack zapewniał wymagane zachowanie.

Testy kontraktu sprawdzają w weryfikacji, czy backend spełnia kontrakt HTTP API, testy integracyjne backendu, czy backend komunikuje się z bazą danych, a test happy path frontendu, czy działa przepływ rejestracji, logowania i pobrania danych aktualnego użytkownika.

### 19.5 Kryteria idempotentności

Za spełnienie kryteriów dotyczących idempotentności odpowiadają pipeline, staging, output oraz cleanup.

Pipeline wykonuje generację jako uporządkowaną listę kroków. Krok zostaje uznany za zakończony dopiero po pełnym sukcesie. Jeśli krok zakończy się błędem, core przerywa generację i uruchamia cleanup całego runa.

Każdy run zaczyna od pustego stagingu, więc ponowne uruchomienie generatora nie zależy od wyniku poprzedniego.

Staging chroni katalog docelowy przed częściowo wygenerowanym projektem. Projekt trafia do katalogu docelowego dopiero po zakończeniu generacji i pozytywnej weryfikacji. Dzięki temu nieudana generacja nie powinna zostawić uszkodzonego wyniku w katalogu docelowym.

### 19.6 Kryteria rozszerzalności

Za spełnienie kryteriów dotyczących rozszerzalności odpowiadają template packi, manifesty, rejestr template packów, kontrakty oraz plan generacji.

Nowa technologia powinna być dodawana jako nowy template pack. Core nie powinien wymagać istotnych zmian przy dodaniu nowego frontendu albo nowego backend-db stacka.

Frontend musi być zgodny z kontraktem HTTP API. Backend-db stack musi być zgodny z kontraktem HTTP API oraz kontraktem danych. Dzięki temu nowe technologie mogą być dodawane niezależnie od istniejących, bez naruszania już obsługiwanych kombinacji.

Manifest template packa określa informacje potrzebne do użycia danej technologii przez generator. Dzięki temu rejestr template packów wykrywa dostępne template packi i ich typy, a planowanie wykrywa konflikty plików między nimi.

## 20 Elementy poza zakresem architektury

Architektura opisuje sposób działania generatora oraz zasady tworzenia wygenerowanego projektu. Nie opisuje elementów, które specyfikacja wymienia w ograniczeniach (15).

Brak tych elementów nie oznacza, że architektura uniemożliwia ich dodanie w przyszłości. Oznacza jedynie, że nie są one wymagane do spełnienia podstawowego zakresu projektu i nie będą podstawą oceny poprawności generatora.

Generator ma tworzyć kompletny, uruchamialny i rozszerzalny szkielet aplikacji webowej, ale nie ma zastępować pełnej platformy deploymentowej ani produkcyjnej infrastruktury serwerowej.
