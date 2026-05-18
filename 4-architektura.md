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
7. Projekt jest weryfikowany i testowany.
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
   Nowa technologia, na przykład kolejny framework frontendowy lub kolejny backend-db stack powinny być dodawane jako nowy template pack, a nie warunki do core generatora. Core sprawdzi dostępne packi i na tej podstawie będzie walidował konfigurację.
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

Core odpowiada za wczytanie konfiguracji, walidację, wybór template packów, zbudowanie planu generacji, zarządzanie wykonaniem kroków pipeline'u, obsługę stanu, staging, finalizację outputu i statystyki. Core nie powinien zawierać szczegółowej logiki konkretnych frameworków.

### Pipeline

Pipeline to uporządkowana lista kroków generacji wykorzystywana przez core.

Pipeline nie jest samodzielnym silnikiem wykonawczym. Nie zarządza globalnym stanem, obsługą błędów ani finalizacją outputu. Te decyzje należą do core. Pipeline określa kolejność kroków i pozwala core przechodzić przez proces generacji w kontrolowany sposób.

### Pipeline state / Stan generacji

Zapisany stan generacji zarządzany przez core.

Stan przechowuje informacje o wykonanych krokach, aktualnym statusie generacji, błędach, użytej konfiguracji, hashu konfiguracji oraz ścieżkach katalogów roboczych. Dzięki temu core może wznowić działanie po błędzie od ostatniego poprawnie zakończonego kroku.

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

### Validation

Proces sprawdzania, czy ze wstępnej konfiguracji użytkownika da się stworzyć obsługiwany projekt.

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

### 3.1 Przepływ i główne etapy działania

1. Pozyskanie danych wejściowych.
   Generator zaczyna od otrzymania danych wejściowych. To jest jedynie deklaracja od użytkownika, co chce uzyskać:
    - nazwa projektu
    - katalog docelowy
    - frontend
    - backend
    - porty
    - zmienne środowiskowe

2. Normalizacja konfiguracji
   Generator przerabia dane wejściowe na spójną konfigurację wewnętrzną za pomocą wspólnego mechanizmu normalizacji danych wejściowych. Wartości zostają uporządkowane i zostaje z nich utworzony docelowy plik konfiguracyjny, na którego podstawie powstanie projekt. Dzięki temu zarówno kreator, jak i plik konfiguracyjny mogą być interpretowane tak samo.

3. Walidacja
   Generator waliduje konfigurację i sprawdza, czy jest ona obsługiwana. Sprawdza, czy istnieje wskazany frontend i backend, czy kombinacja jest wspierana, czy porty nie mają konfliktów oraz czy da się stworzyć output_dir.

4. Wybór elementów generacji
   Po walidacji konfiguracja zamieniana jest na konkretne elementy, które zostaną użyte. To już jest docelowa instrukcja dla generatora, co powstanie jako ostateczna wersja.
   Na tym etapie zostają wybrane odpowiednie template packi oraz elementy wspólne.

5. Stworzenie planu generacji
   Na tym etapie generator buduje plan działania. Określa, jakie pliki zostaną utworzone, które template'y zostaną wyrenderowane, jakie elementy wspólne mają zostać złożone, jakie zmienne będą dostępne w kontekście renderowania oraz jakie kroki pipeline'u i weryfikacji zostaną wykonane przez core. Plan generacji powinien też wykryć konflikty między packami - na przykład jeśli chcą wyrenderować ten sam plik. Odróżnia renderowanie pliku od składania go z kilku packów.

6. Generowanie w katalogu roboczym
   Generator nie zaczyna od katalogu docelowego, ale robi staging. Tam zostaje przeprowadzony cały proces - renderowanie template'ów, tworzenie struktury katalogów, zapis plików i przygotowanie konteneryzacji. To tutaj nastąpi weryfikacja.

7. Weryfikacja
   Etap sprawdzenia, czy wygenerowany projekt rzeczywiście spełnia wymagania. Jest to główne odróżnienie tego generatora od prostego kopiowania template'ów. Poprawność projektu nie jest oceniana tym, że pliki powstały, tylko tym, że przechodzą wymagane testy.
   Weryfikacja sprawdza, czy Docker Compose uruchamia kontenery, backend odpowiada na GET /health, backend komunikuje się z bazą, frontend komunikuje się z backendem, wszystkie testy przechodzą i happy path logowania na użytkownika testowego lub startowego działa.

8. Finalizacja
   Ostatni etap, przenoszący zweryfikowany projekt do docelowego katalogu. Jeśli weryfikacja nie zakończy się sukcesem, projekt nie zostaje przeniesiony do katalogu docelowego.

### 3.2 Tryb kreatora

Tryb CLI, zbierający dane wejściowe od użytkownika definiujące projekt.

### 3.3 Tryb pliku konfiguracyjnego

Tryb użycia jedynie nieinteraktywnego pliku konfiguracyjnego definiującego projekt.

## 4. Główne zasady architektoniczne

### 4.1 Frontend zależy wyłącznie od kontraktu HTTP API

Frontend nie wie nic o tym, jaki backend został wybrany. Dla frontendu istotne jest jedynie to, żeby backend wystawiał mu określone endpointy. Dzięki temu, rozszerzanie generatora o wsparcie dla dowolnych frontendów jest bardzo proste - ponieważ frontend pełni rolę warstwy prezentacji oraz klienta korzystającego z publicznego API backendu.

### 4.2 Backend i baza danych tworzą backend-db stack

Być może na papierze wygodne byłoby rozdzielenie backendu i bazy danych, żeby tworzyć dowolne kombinacje. Niestety, backend ma zbyt duży wpływ na sposób działania bazy danych:

- ORM
- migracje
- modele
- auth
- seedowanie
- tabele techniczne
- testy backend-db

To wszystko sprawia, że obsługa takiej macierzy kombinacji szybko stałaby się nienatywna i pełna sztucznych warunków. Stąd decyzja o utrzymaniu backendu i bazy danych jako jednego backend-db stacka.

### 4.3 PostgreSQL jako stały element infrastruktury

Jest to świadome ograniczenie zakresu pracy. Użytkownik nie będzie mógł w podstawowej wersji wybrać nic innego poza PostgreSQL. Jego decyzją będzie stack Django + PostgreSQL lub FastAPI + PostgreSQL. Dodanie większej liczby obsługiwanych stacków nie powinno wymagać zmiany założeń architektonicznych, ale zwiększyłoby ilość pracy implementacyjnej, testowej i dokumentacyjnej oraz spowoduje konieczność żmudnego dodawania kolejnych stacków jeden po drugim. Dlatego podstawowa wersja pracy zawierać będzie jedynie dwa powyższe stacki.

### 4.4 Kontrakty zamiast adapterów

Ta zasada chroni projekt przed sztuczną warstwą abstrakcji, jaką byłby dowolny adapter. Nie chcę, żeby projekt miał dodatkowe adaptery tylko dlatego, że generator obsłuży inne kombinacje. Dzięki temu spójność zostanie osiągnięta przez kontrakty:

- Frontend jest kompatybilny z backendem, bo spełniają kontrakt API,
- Backend-db stack jest zgodny z wymaganiami projektu, bo spełnia kontrakt danych.

Dzięki temu nie trzeba będzie dodawać sztucznych adapterów, bo kontrakty zapewnią spójność, a template packi zachowają natywność wygenerowanego kodu.

### 4.5 Natywność template packów

Template pack będzie generował kod, który jest naturalny dla danej technologii. Django nie zostanie wciśnięte w typową strukturę FastAPI, a Vue nie będzie udawać Reacta. Dlatego kluczowe będzie dokładne zapoznanie się ze wzorcami standardowymi dla obsługiwanych technologii, a następnie utworzenie każdego template packa zgodnie z nimi. Przykład konwencji:

- Django -> Django ORM, migracje Django, struktura Django
- FastAPI -> struktura FastAPI, osobna konfiguracja aplikacji, osobne modele/schemy
- Vue -> Vue Router, Vite, struktura typowa dla Vue
- React -> React Router, Vite, struktura typowa dla Reacta

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

## 5. Podział systemu na główne części

### 5.1 Core

Core jest głównym modułem sterującym generatora. Core nie może znać szczegółów frameworków, z jakich korzysta. Musi on orkiestrować cały proces generacji:

- uruchomienie CLI
- wczytanie danych
- normalizacja konfiguracji
- walidacja
- planning
- zarządzanie wykonaniem kroków pipeline'u
- zapis i odczyt stanu generacji
- obsługa błędów
- przekazanie wyniku do outputu
- zebranie statystyk

Dzięki temu, w przypadku rozszerzania o kolejne technologie, core nie powinien wymagać istotnych modyfikacji.

### 5.2 Contracts

To nie jest kod aplikacji, a jedynie warstwa wspólnych wymagań, które mają spełnić poszczególne template packi. Dzięki temu wygenerowany projekt pozostaje spójny, a natywność zapewniają konkretne template packi.

Dwa najważniejsze kontrakty:

- kontrakt HTTP API
- kontrakt danych backend-db

### 5.3 Template packs

Część systemu, która dostarcza kod i konfigurację dla konkretnych technologii. Template packi znają szczegóły frameworków, mieści się w nich docelowa struktura generowanego kodu.
Template packi powinny być możliwie niezależne od siebie i komunikować się przez kontrakty oraz contributions. Jeśli autor chce rozszerzyć generator o obsługę kolejnej technologii, po prostu dodaje kolejny template pack. To tam mieści się cały kod, konfiguracja, obsługa kontraktów. Dzięki temu, wystarczy w zasadzie dobrze znać wybrany framework, żeby móc utworzyć dla niego template pack.
Istnieją różne rodzaje template packów (więcej w rozdziale 10.). Template pack zawiera pełne templaty plików oraz templaty contributions, gdzie docelowy plik powstaje ze wszystkich kontrybuujących do niego templatów.

### 5.4 Planning

Część odpowiedzialna za przetłumaczenie konfiguracji na plan generacji. Na tym etapie konfiguracja zostaje zamieniona na zestaw template packów, contributions, kroków generacji i danych potrzebnych do renderowania. Dzięki niemu proces jest przewidywalny i deterministyczny oraz gwarantuje poprawny plan.

### 5.5 Rendering

Proces zmieniający templaty wybrane w planie generacji na realne pliki w katalogu. Renderer przyjmuje template packi i renderuje pełne pliki oraz pliki składane z contributions.

### 5.6 Output

Output odpowiada za fizyczny zapis wyniku, zarówno do stagingu, jak i do katalogu docelowego. Pilnuje też, żeby wynikowa struktura nie była uszkodzona.

Zadania outputu:

- zapewnienie pustego katalogu roboczego
- zapis plików
- przeniesienie projektu do docelowego katalogu
- czyszczenie po błędzie zgodnie z decyzją core
- ochrona docelowego katalogu przed uszkodzonym wynikiem

### 5.7 State

Zapisany stan działania generatora. Bezpieczne korzystanie ze stanów jest możliwe, ponieważ zakładamy, że wynik dla każdej konfiguracji jest deterministyczny. Dzięki temu, core może łatwo wstrzymać i przywrócić proces, obsłużyć błąd w jednym z kroków i powtórzyć krok bez konieczności powtarzania całego procesu generacji oraz łatwo wyczyścić stan i rozpocząć od nowa. Stan pozwala wykryć, czy konfiguracja została zmieniona. Jeśli hash konfiguracji nie zgadza się ze stanem zapisanym z poprzedniego przebiegu, core nie wznawia działania, tylko czyści stan i rozpoczyna proces od nowa.

### 5.8 Verification

Weryfikacja sprawdza, czy projekt w stagingu działa poprawnie. Wygenerowany projekt, zanim trafi do folderu docelowego, jest dokładnie sprawdzany w folderze stagingu. Dzięki temu nie wprowadzamy niedziałającego projektu do katalogu docelowego. Weryfikacja jest wykonywana jako jeden lub kilka kroków pipeline'u zarządzanego przez core.

### 5.9 Statistics

Część odpowiedzialna za mierzenie i raportowanie przebiegu generacji. Statystyki zbierają:

- czas całej generacji
- czas poszczególnych etapów
- wybraną kombinację technologiczną
- liczbę wygenerowanych plików
- liczbę użytych template packów
- status verification
- informację o błędzie, jeśli wystąpił

Mogą też służyć do porównywania czasu trwania etapów oraz czasu generacji różnych kombinacji technologicznych.

## 6. Core generatora

### 6.1 Odpowiedzialność core

Core odpowiada za przebieg całej generacji.
Core orkiestruje:

- uruchomienie generatora
- obsługę trybu kreatora i configu
- wczytanie danych wejściowych
- normalizację konfiguracji
- walidację konfiguracji
- dobór template packów
- zbudowanie planu generacji
- zarządzanie wykonaniem kroków pipeline'u
- obsługę błędów
- zapis i odczyt stanu
- przekazanie wyniku do outputu
- wykonanie kroku lub kroków verification w ramach pipeline'u
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

CLI jest wejściem użytkownika do generatora. Jest podmodułem core'a i jego zadaniem jest jedynie pozyskanie ustrukturyzowanych danych wejściowych i przekazanie ich dalej. CLI wyświetla też użytkownikowi stan generacji.
CLI obsługuje trzy tryby wejścia:

- tryb kreatora
- tryb pliku konfiguracyjnego
- tryb wznowienia

CLI wyświetla użytkownikowi:

- stan generacji
- postęp generacji
- błędy w procesie generacji
- statystyki z procesu generacji

### 6.4 Ładowanie konfiguracji

Kiedy CLI już przygotuje dane wejściowe, przekazuje je do core'a. Dane są sprawdzane pod kątem poprawności struktury i syntaktyki, a następnie przekazywane do modułu normalizacji konfiguracji.

### 6.5 Normalizacja konfiguracji

W tym module konfiguracja zostaje uporządkowana i znormalizowana. Wynikiem normalizacji powinien być docelowy model konfiguracji: uporządkowany, uzupełniony o dane domyślne i poprawny semantycznie. Poprawność semantyczna oznacza tutaj spójne znaczenie danych, a nie potwierdzenie, że dana technologia lub kombinacja jest obsługiwana przez generator.
Normalizacja obejmuje:

- uzupełnienie domyślnych portów
- ujednolicenie nazw technologii
- zamiana ścieżki względnej na docelową ścieżkę output_dir
- uzupełnienie domyślnych wartości env
- utworzenie slug/nazwy technicznej projektu

### 6.6 Walidacja konfiguracji

Walidacja sprawdza, czy z tej konfiguracji można bezpiecznie wygenerować projekt. Ten etap upewnia się, że wszystkie technologie zawarte w konfigu są obsługiwane, a także nie mają konfliktów.
Walidacja obejmuje sprawdzenie:

- czy frontend jest obsługiwany
- czy backend jest obsługiwany
- czy kombinacja technologiczna jest wspierana
- czy porty nie mają konfliktów
- czy output_dir jest poprawny
- czy wymagane wartości env istnieją albo mogą zostać wygenerowane
- czy istnieją template packi potrzebne dla tej konfiguracji
- czy z manifestów packów wynika ich kompatybilność i brak konfliktów

### 6.7 Budowanie planu generacji

Plan generacji przekłada język konfiguracji na docelowy plan wykonania, używający już konkretnych zasobów.
Plan określa:

- wybrane template packi
- pliki właścicielskie
- pliki składane z contributions
- kontekst renderowania
- kroki pipeline'u
- kroki verification
- wykryte zależności i kolejność działań

### 6.8 Pipeline jako podmoduł core

### 6.9 Zarządzanie wykonaniem kroków pipeline'u

### 6.10 Zarządzanie stanem generacji

### 6.11 Obsługa błędów i przerwania generacji

### 6.12 Wznawianie generacji

### 6.13 Przekazanie wyniku do outputu

### 6.14 Uruchomienie verification

### 6.15 Zbieranie statystyk

## 7. Pipeline zarządzany przez core

### 7.1 Rola pipeline'u w architekturze

### 7.2 Pipeline jako uporządkowana lista kroków

### 7.3 Granice odpowiedzialności pipeline'u

### 7.4 Krok pipeline'u

### 7.5 Kolejność kroków pipeline'u

### 7.6 Relacja pipeline'u z core

### 7.7 Relacja pipeline'u z generation plan

### 7.8 Pomijanie kroków przy wznowieniu

### 7.9 Podstawowy przebieg pipeline'u

## 8. Stan generacji

### 8.1 Rola stanu generacji

### 8.2 Stan jako mechanizm zarządzany przez core

### 8.3 Informacje zapisywane w stanie

### 8.4 Hash konfiguracji

### 8.5 Lista ukończonych kroków

### 8.6 Informacja o aktualnym kroku

### 8.7 Informacja o błędzie

### 8.8 Wznawianie generacji na podstawie stanu

### 8.9 Zachowanie po zmianie konfiguracji

### 8.10 Czyszczenie stanu

## 9. Staging i output

### 9.1 Rola stagingu

### 9.2 Katalog roboczy generacji

### 9.3 Katalog finalny projektu

### 9.4 Zasada braku częściowego wyniku w final output

### 9.5 Finalizacja poprawnej generacji

### 9.6 Czyszczenie po błędzie

### 9.7 Relacja outputu ze stanem generacji

## 10. Idempotentność i deterministyczność

### 10.1 Idempotentność generacji

### 10.2 Deterministyczność wyniku strukturalnego

### 10.3 Wartości losowe i sekrety

### 10.4 Ponowne uruchomienie dla tej samej konfiguracji

### 10.5 Wznawianie po błędzie

### 10.6 Ochrona przed niespójnym wynikiem

## 11. Konfiguracja wejściowa

### 11.1 Minimalny zestaw danych wejściowych

### 11.2 Konfiguracja projektu

### 11.3 Konfiguracja frontendu

### 11.4 Konfiguracja backendu

### 11.5 Konfiguracja bazy danych

### 11.6 Konfiguracja portów

### 11.7 Konfiguracja środowiskowa

### 11.8 Wartości domyślne

### 11.9 Docelowy model konfiguracji

## 12. Walidacja i obsługa błędów

### 12.1 Walidacja danych wejściowych

### 12.2 Walidacja kombinacji technologicznych

### 12.3 Walidacja portów

### 12.4 Walidacja zmiennych środowiskowych

### 12.5 Walidacja ścieżki output_dir

### 12.6 Walidacja kompatybilności template packów

### 12.7 Komunikaty błędów

### 12.8 Przerwanie generacji przed zapisem plików

## 13. Model kontraktów

### 13.1 Rola kontraktów w architekturze

### 13.2 Kontrakt HTTP API

### 13.3 Kontrakt danych backend-db

### 13.4 Wersjonowanie kontraktów

### 13.5 Zgodność template packów z kontraktami

### 13.6 Testowanie zgodności z kontraktami

## 14. Template'y i template packi

### 14.1 Rola template'ów

### 14.2 Rola template packów

### 14.3 Template pack jako jednostka rozszerzalności

### 14.4 Manifest template packa

### 14.5 Template'y właścicielskie

### 14.6 Template'y składane

### 14.7 Contributions do plików wspólnych

### 14.8 Ograniczenie logiki w template'ach

## 15. Rodzaje template packów

### 15.1 Frontend pack

### 15.2 Backend-db pack

### 15.3 Infrastructure pack

### 15.4 Common pack

### 15.5 Verification pack

## 16. Wybór template packów

### 16.1 Rejestr template packów

### 16.2 Dobór frontend packa

### 16.3 Dobór backend-db packa

### 16.4 Dobór infrastructure packa

### 16.5 Dobór common packów

### 16.6 Wykrywanie niewspieranych kombinacji

### 16.7 Wykrywanie konfliktów między packami

## 17. Łączenie template packów

### 17.1 Generation plan jako wynik doboru packów

### 17.2 Kolejność generowania elementów projektu

### 17.3 Łączenie plików właścicielskich

### 17.4 Łączenie plików składanych

### 17.5 Składanie docker-compose.yml

### 17.6 Składanie .env i .env.example

### 17.7 Składanie README.md

### 17.8 Obsługa konfliktów plików

## 18. Rendering

### 18.1 Rola renderingu

### 18.2 Kontekst renderowania

### 18.3 Renderowanie plików właścicielskich

### 18.4 Renderowanie plików składanych

### 18.5 Renderowanie contributions

### 18.6 Ograniczenie logiki w rendererze

## 19. Backend-db stack

### 19.1 Uzasadnienie sprzężenia backendu i bazy danych

### 19.2 FastAPI + PostgreSQL

### 19.3 Django + PostgreSQL

### 19.4 Minimalny kontrakt danych

### 19.5 Rozszerzenia schemy specyficzne dla frameworka

### 19.6 Migracje

### 19.7 Dane startowe lub testowe do logowania

## 20. Verification

### 20.1 Rola verification

### 20.2 Verification jako krok pipeline'u zarządzany przez core

### 20.3 Verification wygenerowanego projektu

### 20.4 Verification kontraktu HTTP API

### 20.5 Verification kontraktu danych

### 20.6 Verification Docker Compose

### 20.7 Verification testów

### 20.8 Verification macierzy wspieranych kombinacji

### 20.9 Zachowanie po nieudanej verification

## 21. Statistics

### 21.1 Rola statystyk

### 21.2 Statystyki zbierane przez core

### 21.3 Statystyki kroków pipeline'u

### 21.4 Statystyki verification

### 21.5 Raport końcowy generacji

## 22. Struktura katalogów generatora

### 22.1 Proponowana struktura główna

### 22.2 Katalog core

### 22.3 Katalog contracts

### 22.4 Katalog template_packs

### 22.5 Katalog verification

### 22.6 Katalog tests

### 22.7 Katalog docs

## 23. Struktura wygenerowanego projektu

### 23.1 Struktura root projektu

### 23.2 Struktura frontendu

### 23.3 Struktura backendu

### 23.4 Pliki środowiskowe

### 23.5 Pliki Docker

### 23.6 README.md

### 23.7 Testy

## 24. Rozszerzalność generatora

### 24.1 Dodanie nowego frontendu

### 24.2 Dodanie nowego backendu

### 24.3 Dodanie nowej bazy danych

### 24.4 Zgodność rozszerzeń z kontraktami

### 24.5 Brak regresji w istniejących kombinacjach

### 24.6 Ograniczenie zmian w core

### 24.7 Dokumentowanie rozszerzeń

## 25. Jakość architektury

### 25.1 SOLID w generatorze

### 25.2 DRY w generatorze

### 25.3 Open/closed principle

### 25.4 Natywność wygenerowanego kodu

### 25.5 Czytelność i samodokumentujący się kod

### 25.6 Granice odpowiedzialności modułów

## 26. Bezpieczeństwo aplikacyjne w zakresie projektu

### 26.1 JWT

### 26.2 Hashowanie haseł

### 26.3 CORS

### 26.4 Zmienne środowiskowe

### 26.5 Zakres bezpieczeństwa poza projektem

## 27. Decyzje i kompromisy architektoniczne

### 27.1 Dlaczego frontend jest niezależny od backendu

### 27.2 Dlaczego backend i baza są sprzężone

### 27.3 Dlaczego PostgreSQL jest stałym elementem infrastruktury

### 27.4 Dlaczego kontrakty zamiast adapterów

### 27.5 Dlaczego dopuszczalne są kontrolowane powtórzenia

### 27.6 Dlaczego pipeline jest zarządzany przez core

### 27.7 Dlaczego wygenerowany projekt nie zależy od generatora

## 28. Powiązanie architektury z kryteriami akceptacyjnymi

### 28.1 Kryteria generatora

### 28.2 Kryteria wspieranych kombinacji

### 28.3 Kryteria wygenerowanego projektu

### 28.4 Kryteria kontraktów

### 28.5 Kryteria idempotentności i wznawiania

### 28.6 Kryteria rozszerzalności

## 29. Elementy poza zakresem architektury
