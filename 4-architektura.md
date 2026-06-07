# Architektura

Stan: 28.05.2026

## 1 Wstęp

### 1.1 Cel dokumentu

Dokument przedstawia architekturę generatora oraz najważniejsze decyzje projektowe. Nie narzuca szczegółów technicznych implementacji, ale narzuca podział odpowiedzialności.

### 1.2 Architektura w skrócie

Skrócony przepływ od uruchomienia generatora do gotowego projektu:

1. Użytkownik definiuje, jaki projekt chce otrzymać.
2. Generator zamienia to na konfigurację.
3. Konfiguracja zostaje walidowana.
4. Wybierane są odpowiednie template packi.
5. Projekt powstaje w katalogu roboczym.
6. Projekt jest weryfikowany i testowany.
7. Projekt trafia do finalnego katalogu.

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
   Nieudana generacja nie może zostawić pozostałości w docelowym katalogu. Ponowne uruchomienie generatora dla tej samej konfiguracji powinno prowadzić do tej samej struktury projektu i nie może uszkadzać istniejącego wyniku. Wznowienie powinno następować od ostatniego poprawnie zakończonego kroku.

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

### 2.3 Konfiguracja

Zestaw danych wejściowych opisujących, jaki projekt ma zostać wygenerowany.

Konfiguracja może pochodzić z kreatora albo z pliku konfiguracyjnego. Zawiera między innymi nazwę projektu, katalog docelowy, wybrany frontend, wybrany backend, bazę danych, porty oraz wartości środowiskowe.

### 2.4 Kontrakt HTTP API

Zbiór wymagań określających sposób komunikacji pomiędzy frontendem i backendem.

Kontrakt HTTP API definiuje wymagane endpointy, format requestów, format response'ów, statusy HTTP oraz sposób użycia tokena JWT. Dzięki temu frontend nie musi znać konkretnej implementacji backendu i może komunikować się z każdym backendem spełniającym ten sam kontrakt.

### 2.5 Kontrakt danych backend-db

Zbiór minimalnych wymagań wobec backend-db stacka dotyczących danych wymaganych do działania aplikacji.

Kontrakt danych określa, że backend-db stack musi zapewnić minimalny model użytkownika pozwalający na jednoznaczną identyfikację użytkownika, rejestrację za pomocą emaila, logowanie za pomocą emaila, weryfikację hasła zapisanego jako hash oraz oznaczenie użytkownika jako aktywnego lub nieaktywnego.

Kontrakt danych nie wymaga identycznej fizycznej struktury tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez wybrany framework.

### 2.6 Template

Pojedynczy szablon pliku albo fragmentu pliku używany podczas generacji projektu.

Template może opisywać na przykład plik konfiguracyjny, plik źródłowy, test, fragment README.md albo fragment docker-compose.yml. Template nie powinien zawierać logiki wyboru technologii. Wybór technologii odbywa się wcześniej, na poziomie konfiguracji, rejestru template packów i planu generacji.

### 2.7 Template pack

Zestaw template'ów i manifestu odpowiadający za wygenerowanie konkretnej części projektu.

Template pack jest podstawową jednostką rozszerzalności generatora. Nowa technologia, na przykład nowy frontend albo nowy backend-db stack, powinna być dodawana jako nowy template pack, a nie jako dodatkowa logika warunkowa w core generatora.

### 2.8 Manifest template packa

Opis template packa zawierający informacje potrzebne generatorowi do jego użycia.

Manifest określa między innymi typ template packa, obsługiwaną technologię, wymagane kontrakty, zapewniane funkcjonalności, wymagane dane wejściowe, generowane pliki oraz kompatybilność z innymi elementami generatora.

### 2.9 Template registry

Rejestr dostępnych template packów, tworzony podczas procesu generacji.

Template registry pozwala generatorowi sprawdzić, jakie template packi są dostępne, które technologie obsługują, z jakimi kontraktami są zgodne i czy mogą zostać użyte dla wybranej konfiguracji. Dzięki temu core generatora nie musi znać szczegółów konkretnych frameworków.

### 2.10 Backend-db stack

Sprzężona para backendu i bazy danych traktowana jako jedna jednostka generacji.

Backend i baza danych są łączone w backend-db stack, ponieważ wybór backendu wpływa na ORM, migracje, modele, auth, strukturę danych wymaganą do uwierzytelniania, tabele techniczne oraz testowanie komunikacji z bazą. Przykładami backend-db stacków są FastAPI + SQLite oraz Django + PostgreSQL.

### 2.11 Core

Główna część generatora odpowiedzialna za obsługę procesu generacji.

Core odpowiada za wczytanie konfiguracji, walidację, wybór template packów, zbudowanie planu generacji, zarządzanie wykonaniem kroków pipeline'u, obsługę stanu, staging, finalizację outputu i statystyki. Core nie powinien zawierać szczegółowej logiki konkretnych frameworków.

### 2.12 Pipeline

Pipeline to uporządkowana lista kroków generacji wykorzystywana przez core.

Pipeline nie jest samodzielnym silnikiem wykonawczym. Nie zarządza globalnym stanem, obsługą błędów ani finalizacją outputu. Te decyzje należą do core. Pipeline określa kolejność kroków i pozwala core przechodzić przez proces generacji w kontrolowany sposób.

### 2.13 Stan generacji

Zapisany stan generacji zarządzany przez core.

Stan przechowuje informacje o wykonanych krokach, aktualnym statusie generacji, błędach, użytej konfiguracji, hashu konfiguracji oraz ścieżkach katalogów roboczych. Dzięki temu core może wznowić działanie po błędzie od ostatniego poprawnie zakończonego kroku.

### 2.14 Generation plan

Plan technicznego wykonania generacji utworzony na podstawie konfiguracji i dobranych template packów. Jest zbiorem parametrów dla kroków pipeline'u.

Generation plan określa, jakie template packi zostaną użyte, jakie pliki zostaną wygenerowane, jakie contributions zostaną dodane do plików wspólnych.

### 2.15 Contribution

Wkład template packa lub templata do pliku albo elementu, który jest składany z wielu źródeł.

Contribution jest używane tam, gdzie jeden plik powstaje z informacji dostarczanych przez wiele template packów. Przykładami takich plików są docker-compose.yml, .env oraz README.md.

### 2.16 Staging

Katalog roboczy, w którym generator tworzy projekt przed zapisaniem go do finalnego katalogu.

Staging chroni katalog docelowy przed częściowo wygenerowanym lub uszkodzonym wynikiem. Projekt trafia do final output dopiero po poprawnym zakończeniu wymaganych kroków pipeline'u.

### 2.17 Final output

Finalny katalog projektu przekazywany użytkownikowi po zakończeniu generacji.

Final output powinien zawierać wyłącznie poprawnie wygenerowany i zweryfikowany projekt. Nieudana generacja nie powinna zostawiać częściowego wyniku w final output.

### 2.18 Validation

Proces sprawdzania, czy ze wstępnej konfiguracji użytkownika da się stworzyć obsługiwany projekt.

### 2.19 Verification

Proces sprawdzania, czy wygenerowany projekt spełnia wymagania.

Verification obejmuje między innymi sprawdzenie uruchomienia projektu przez Docker Compose, działanie kontraktu HTTP API, działanie kontraktu danych, komunikację frontend-backend, komunikację backend-db oraz przejście wymaganych testów.

### 2.20 Idempotentność

Właściwość generatora oznaczająca, że ponowne uruchomienie dla tej samej konfiguracji nie prowadzi do niespójnego lub częściowo uszkodzonego projektu.

Idempotentność jest szczególnie ważna przy błędach generacji, wznowieniu pipeline'u i ponownym uruchamianiu generatora dla tej samej konfiguracji.

### 2.21 Deterministyczność

Właściwość generatora oznaczająca, że ta sama konfiguracja powinna prowadzić do takiej samej struktury wygenerowanego projektu.

Deterministyczność dotyczy przede wszystkim struktury katalogów, wygenerowanych plików, dobranych template packów i planu generacji. Wartości losowe, takie jak sekrety, powinny być jawnie zapisane albo generowane w kontrolowany sposób.

### 2.22 Artefakt

Folder lub plik tworzony przy przejściu między stanami generacji.

## 3 Ogólny model działania generatora

### 3.1 Przepływ i główne etapy działania

1. Pozyskanie danych wejściowych.
   Generator zaczyna od otrzymania danych wejściowych. To jest jedynie deklaracja od użytkownika, co chce uzyskać:
    - nazwa projektu
    - katalog docelowy
    - frontend
    - backend-db stack
    - porty
    - zmienne środowiskowe

2. Normalizacja konfiguracji
   Generator przerabia dane wejściowe na spójną konfigurację wewnętrzną za pomocą wspólnego mechanizmu normalizacji danych wejściowych. Wartości zostają uporządkowane i zostaje z nich utworzony docelowy plik konfiguracyjny, na którego podstawie powstanie projekt. Dzięki temu zarówno kreator, jak i plik konfiguracyjny mogą być interpretowane tak samo.

3. Walidacja
   Generator waliduje konfigurację i sprawdza, czy jest ona obsługiwana. Sprawdza, czy istnieje wskazany frontend i backend, czy porty nie mają konfliktów oraz czy da się stworzyć output_dir.

4. Stworzenie planu generacji
   Plan generacji jest zbiorem danych parametryzujących generację projektu. Zostanie on przekazany do pipeline'u. Plan generacji powinien wykryć konflikty między packami - na przykład jeśli chcą wyrenderować ten sam plik. Odróżnia renderowanie pliku od składania go z kilku packów, informuje, jakie pliki składane zostaną stworzone.

5. Generowanie w katalogu roboczym
   Generator nie zaczyna od katalogu docelowego, ale robi staging. Na podstawie stałej listy kroków oraz planu generacji zostaje przeprowadzony cały proces - renderowanie template'ów, tworzenie struktury katalogów, zapis plików i przygotowanie konteneryzacji.

6. Weryfikacja
   Etap sprawdzenia, czy wygenerowany projekt rzeczywiście spełnia wymagania. Jest to główne odróżnienie tego generatora od prostego kopiowania template'ów. Poprawność projektu nie jest oceniana tym, że pliki powstały, tylko tym, że przechodzą wymagane testy.
   Weryfikacja sprawdza, czy Docker Compose uruchamia wymagane kontenery, backend odpowiada na GET /health, backend komunikuje się z bazą, frontend komunikuje się z backendem, wszystkie testy przechodzą oraz happy path rejestracji, logowania i pobrania danych aktualnego użytkownika działa.

7. Finalizacja
   Ostatni etap, przenoszący zweryfikowany projekt do docelowego katalogu. Jeśli weryfikacja nie zakończy się sukcesem, projekt nie zostaje przeniesiony do katalogu docelowego.

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

## 5 Podział systemu na główne części

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

### 5.2 Pipeline

Zarządzany przez core iterowalny proces, przechodzący przez renderowanie, weryfikację i output. Pipeline umożliwia przechodzenie ze stanu do stanu w przód, ale też pozwala się cofać.

### 5.3 Template packs

Część systemu, która dostarcza kod i konfigurację dla konkretnych technologii. Template packi znają szczegóły frameworków, mieści się w nich docelowa struktura generowanego kodu.
Template packi powinny być możliwie niezależne od siebie i komunikować się przez kontrakty oraz contributions. Jeśli autor chce rozszerzyć generator o obsługę kolejnej technologii, po prostu dodaje kolejny template pack. To tam mieści się cały kod, konfiguracja, obsługa kontraktów. Dzięki temu, wystarczy w zasadzie dobrze znać wybrany framework, żeby móc utworzyć dla niego template pack.
Istnieją różne rodzaje template packów. Template pack zawiera pełne templaty plików oraz templaty contributions, gdzie docelowy plik powstaje ze wszystkich kontrybuujących do niego templatów.

### 5.4 Planning

Część odpowiedzialna za przetłumaczenie konfiguracji na plan generacji. Na tym etapie konfiguracja zostaje zamieniona na zestaw template packów, contributions i danych potrzebnych do renderowania. Dzięki niemu proces jest przewidywalny i deterministyczny oraz gwarantuje poprawny plan.

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

## 6 Core generatora

### 6.1 Odpowiedzialność core

Core odpowiada za przebieg całej generacji.
Core orkiestruje:

- uruchomienie generatora
- obsługę trybu kreatora i configu
- wczytanie danych wejściowych
- normalizację konfiguracji
- walidację konfiguracji
- zarządzanie wykonaniem kroków pipeline'u
- obsługę błędów
- zapis i odczyt stanu
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

Tutaj konfiguracja zostaje uporządkowana i znormalizowana. Wynikiem normalizacji powinien być docelowy model konfiguracji: uporządkowany, uzupełniony o dane domyślne i poprawny semantycznie. Poprawność semantyczna oznacza tutaj spójne znaczenie danych, a nie potwierdzenie, że dana technologia lub kombinacja jest obsługiwana przez generator.
Normalizacja obejmuje:

- uzupełnienie domyślnych portów
- ujednolicenie nazw technologii
- zamiana ścieżki względnej na docelową ścieżkę output_dir
- uzupełnienie domyślnych wartości env
- utworzenie nazwy technicznej projektu

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
- pliki składane z contributions
- dane projektu

### 6.8 Pipeline jako podmoduł core

Pipeline jest wyrażonym przez listę kroków przechodzeniem pomiędzy kolejnymi stanami. Pipeline definiuje kroki i ich kolejność na podstawie planu generacji. Decyzja, czy przejść dalej, wznowić proces albo przerwać generację, należy do core.

### 6.9 Zarządzanie wykonaniem kroków pipeline'u

Pipeline definiuje kroki bazując na planie generacji i wykonuje je. Core zarządza przebiegiem wykonania, odbiera wynik kroku i decyduje, czy można przejść do kolejnego kroku.

Krok jest uznawany za ukończony dopiero po pełnym sukcesie. Dopiero wtedy core zapisuje stan generacji, w przeciwnym wypadku cofa się i ponawia krok lub rzuca błąd.

### 6.10 Zarządzanie stanem generacji

Każde przejście między stanami może utworzyć artefakty, czyli pliki albo foldery, oraz wywołać efekty uboczne, na przykład uruchomienie kontenerów Docker. Jeśli przejście między stanami zostanie zatrzymane przez błąd, core powinien usunąć artefakty i cofnąć efekty uboczne danego kroku.

Stan zapisuje core, a nie pipeline. Dzięki temu pipeline pozostaje mechanizmem przechodzenia przez kroki, a decyzje o wznowieniu, przerwaniu i zapisie checkpointów należą do core.

### 6.11 Obsługa błędów i przerwania generacji

Jeśli wystąpi błąd, pipeline przekazuje informację o błędzie do core. Core zatrzymuje przechodzenie do kolejnych kroków, zapisuje informację o błędzie i uruchamia cleanup dla nieudanego kroku.

Nieudany krok nie zostaje zapisany jako ukończony. Dzięki temu generację można wznowić od ostatniego stabilnego stanu.

### 6.12 Wznawianie generacji

Wznawianie generacji następuje, gdy core wczyta zapisany stan i rozpocznie iterowanie przez pipeline od pierwszego nieukończonego kroku.

Jeśli konfiguracja zmieniła się od poprzedniego uruchomienia, core nie powinien bezrefleksyjnie wznawiać generacji. W takiej sytuacji stan powinien zostać odrzucony albo proces powinien zakończyć się czytelnym błędem.

Możliwe jest dodanie strategii ponawiania wybranych kroków, ale retry powinno dotyczyć tylko błędów technicznych, które mogą mieć charakter chwilowy.

### 6.13 Zbieranie statystyk

W trakcie generacji są zbierane różne statystyki:

- czas wykonania kroków
- ogólny czas generacji
- liczba błędów i wznowień
- wybrana kombinacja technologiczna
- status verification
- krok, na którym wystąpił błąd

## 7 Pipeline zarządzany przez core

### 7.1 Rola pipeline'u w architekturze

Pipeline jest wyrażonym przez listę kroków przechodzeniem pomiędzy kolejnymi stanami. Definiuje kroki i ich kolejność na podstawie planu generacji. Decyzja, czy przejść dalej, podejmowana jest przez core.

Odpowiedzialności pipeline'u:

- definicja listy kroków
- wykonywanie poszczególnych kroków
- zwracanie wyniku kroku do core

Pipeline nie zapisuje globalnego stanu generacji i nie finalizuje outputu.

### 7.2 Pipeline jako uporządkowana lista kroków

Pipeline definiuje kroki bazując na planie generacji. W zależności od wybranych template packów, niektóre kroki będą odpowiednio sparametryzowane.

Zadania, które zrealizuje pipeline:

1. Pobranie generation planu
2. Przygotowanie stagingu.
3. Wygenerowanie struktury projektu.
4. Renderowanie template'ów i contributions.
5. Wygenerowanie konfiguracji środowiskowej i Docker Compose.
6. Zbudowanie projektu przez Docker Compose.
7. Uruchomienie projektu przez Docker Compose.
8. Uruchomienie migracji albo inicjalizacji bazy, jeśli stack tego wymaga.
9. Uruchomienie testów jednostkowych i integracyjnych.
10. Sprawdzenie happy path rejestracji, logowania i pobrania danych aktualnego użytkownika.
11. Zatrzymanie środowiska verification.
12. Przeniesienie projektu do katalogu docelowego.
13. Wyczyszczenie stagingu.

Generator nie powinien instalować zależności globalnie na komputerze użytkownika. Zależności powinny być instalowane w ramach Docker builda albo wewnątrz kontenerów. Niektóre zależności, jak package-lock.json, muszą być zainstalowane w projekcie.

### 7.3 Granice odpowiedzialności pipeline'u

Pipeline jest narzędziem pomocniczym dla core. Pipeline nie podejmuje decyzji o wznowieniu, przerwaniu procesu, zapisie stanu ani finalizacji outputu.

Jeśli pojawi się błąd, pipeline przekazuje go do core. Core decyduje, czy wykonać cleanup, ponowić krok, przerwać generację albo zwrócić błąd użytkownikowi.

### 7.4 Krok pipeline'u

Krok pipeline'u to przejście ze stanu poprzedzającego do stanu następującego zdefiniowane w liście kroków.

Krok może tworzyć artefakty oraz efekty uboczne. Artefaktami są na przykład pliki i foldery. Efektami ubocznymi mogą być na przykład uruchomione kontenery Docker, wolumeny, sieci albo dane utworzone podczas testów.

Krok powinien mieć określone:

- co wykonuje
- jakie artefakty tworzy
- jakie efekty uboczne może powodować
- po czym poznać, że zakończył się sukcesem
- jak posprzątać po błędzie

### 7.5 Kolejność kroków pipeline'u

Kroki wykonywane są zgodnie z listą utworzoną przez planner na podstawie generation planu.

Podstawowy model pipeline'u jest liniowy. Warunkowe różnice, na przykład obecność osobnego kontenera database dla Django + PostgreSQL i jego brak dla FastAPI + SQLite, powinny wynikać z generation planu oraz manifestów template packów.

### 7.6 Relacja pipeline'u z core

Pipeline to uporządkowany mechanizm kroków, z którego korzysta core.

Core:

- tworzy pipeline na podstawie generation planu
- uruchamia kolejne kroki
- zapisuje stan po sukcesie kroku
- obsługuje błędy
- decyduje o wznowieniu albo przerwaniu procesu

### 7.7 Relacja pipeline'u z generation plan

Kroki pipeline'u zostają zdefiniowane na podstawie generation planu. To generation plan określa, jakie template packi, pliki, contributions i kroki verification są wymagane dla danej konfiguracji.

Dzięki temu pipeline nie musi zawierać logiki konkretnych technologii.

### 7.8 Pomijanie kroków przy wznowieniu

Przy wznowieniu core odczytuje zapisany stan i pomija kroki oznaczone jako ukończone. Pierwszy nieukończony krok jest wykonywany ponownie.

Przed ponownym wykonaniem kroku core powinien upewnić się, że artefakty i efekty uboczne poprzedniej, nieudanej próby zostały usunięte albo mogą zostać bezpiecznie nadpisane.

### 7.9 Podstawowy przebieg pipeline'u

Wzór listy kroków:

- pobranie parametrów z generation planu
- utworzenie folderu stagingu
- utworzenie struktury plików na podstawie manifestów template packów
- utworzenie plików z contributions na podstawie manifestów template packów
- rendering globalnych template packów, na przykład Docker
- rendering template packa backend-db stacka
- rendering template packa frontendu
- wygenerowanie plików zależności backendu i frontendu
- uruchomienie docker compose build
- uruchomienie środowiska przez docker compose
- uruchomienie migracji albo inicjalizacji bazy, jeśli stack tego wymaga
- uruchomienie testów jednostkowych backend-db stacka
- uruchomienie testów jednostkowych frontendu
- uruchomienie testów integracyjnych
- uruchomienie testu typu happy path
- zatrzymanie środowiska Docker Compose
- utworzenie folderu docelowego
- kopia projektu do folderu docelowego
- czyszczenie stagingu

## 8 Stan generacji

### 8.1 Rola stanu generacji

Stan generacji sprawia, że wykonanie pipeline'u można zatrzymywać, wznawiać, powtarzać kroki. Zwiększa to jego odporność na błędy i ułatwi rozszerzanie funkcjonalności.

### 8.2 Stan jako mechanizm zarządzany przez core

Proces generacji zawsze jest w jakimś stanie. Core weryfikuje, czy przejście do stanu kolejnego nastąpiło, i na tej podstawie przełącza stan.

Każde przejście ma zdefiniowane tworzone artefakty oraz skutki uboczne. Dzięki temu stany są deterministyczne, a cofając skutki uboczne i usuwając artefakty, łatwo jest przejść do stanu poprzedniego.

### 8.3 Informacje zapisywane w stanie

Każdy stan składa się z charakteryzujących go artefaktów i efektów ubocznych. Każde dozwolone przejście definiuje listę artefaktów i efektów ubocznych, jakie doda lub usunie. Każdy efekt uboczny zawiera informację, jak go uruchomić i usunąć. Dzięki temu przechodzenie między stanami sprowadza się do dodawania/usuwania artefaktów i włączania/wyłączania efektów ubocznych.

### 8.4 Hash konfiguracji

Każda konfiguracja jest hashowana. Dzięki temu, przed wznowieniem można łatwo sprawdzić, czy wystarczy wznowić (jeśli konfiguracja nie zmieniła się), czy trzeba rozpocząć proces od nowa (jeśli zmieniła się).

### 8.5 Lista ukończonych kroków

Podczas procesu generacji każde przejście zapisuje się w logu przejść. To pozwala przechodzić do stanów poprzednich i wznawiać proces. Przejście zapisuje się do logu przejść po pozytywnym ukończeniu.

### 8.6 Informacja o aktualnym kroku

Informacja o kroku aktualnym jest przechowywana w osobnym miejscu, niż historia. Jest tu też przechowywana pełna lista artefaktów i skutków ubocznych, które powinny obowiązywać po ukończeniu kroku. Dzięki temu, w przypadku niepowodzenia, od razu wiadomo, jak cofnąć zmiany, łatwo też zweryfikować, czy krok powiódł się.

### 8.7 Informacja o błędzie

Błąd wstrzymuje wykonanie kroku i jest przekazywany do core'a. To core zdecyduje, czy krok jest ponawiany i co robić dalej.

### 8.8 Wznawianie generacji na podstawie stanu

Jeśli core podejmie decyzję o wznowieniu generacji, stan jest zrównywany do tego z ostatniego ukończonego kroku. Zostają usunięte artefakty i wstrzymane/uruchomione skutki uboczne. Od tego miejsca można deterministycznie kontynuować run.

## 9 Staging i output

### 9.1 Rola stagingu

Staging zapewnia, że katalog docelowy nie zostaje zaśmiecony niedziałającym projektem. Staging znajduje się w tymczasowym folderze domyślnym. Przy uruchomieniu nowego runa staging jest zawsze czyszczony. Gwarantuje to, że na dysku nie pozostanie żaden niesprawdzony, niedziałający efekt generacji.

### 9.2 Katalog roboczy generacji

Katalog roboczy to domyślny folder TEMP.

### 9.3 Katalog finalny projektu

Zdefiniowany przez użytkownika.

### 9.4 Finalizacja poprawnej generacji

Po udanej generacji i zakończeniu weryfikacji, projekt zostaje bezpośrednio skopiowany do folderu końcowego.

### 9.5 Czyszczenie po błędzie

W przypadku błędu i decyzji o niewznawianiu runa, wystarczy wyczyścić zawartość folderu TEMP.

## 10 Konfiguracja wejściowa

### 10.1 Zestaw danych wejściowych

Dane wejściowe zawsze będą zawierały:

- nazwa projektu
- katalog docelowy
- frontend
- backend-db stack
- porty do wykorzystania
- zmienne środowiskowe

### 10.2 CLI vs plik konfiguracyjny

Oba zakończą się utworzeniem identycznej konfiguracji. Różnice są wyłącznie w zachowaniu.

CLI normalizuje i weryfikuje dane wprowadzone w każdym kroku i od razu daje użytkownikowi możliwość poprawienia danych.
Plik konfiguracyjny jest sprawdzany jako całość. Niepoprawny plik kończy się rzuceniem błędu z informacją, co należy zmienić.

### 10.3 Konfiguracja projektu

Ścieżka bezwzględna do katalogu docelowego oraz jego nazwa.

Ścieżka musi prowadzić do istniejącego miejsca na dysku, a katalog musi umożliwiać zapis i odczyt plików.

### 10.4 Konfiguracja frontendu

Wybór template packa z dostępnych frontendów. Plik konfiguracyjny jest walidowany pod kątem dostępności, CLI pozwala wybrać tylko spośród dostępnych.

### 10.5 Konfiguracja backend-db stacka

Wybór template packa z dostępnych backendów. Plik konfiguracyjny jest walidowany pod kątem dostępności, CLI pozwala wybrać tylko spośród dostępnych.

### 10.6 Konfiguracja portów

Plik konfiguracyjny wymaga podania portów pod oczekiwane usługi. CLI będzie od razu weryfikowało, czy port jest dostępny. Nie można użyć niedostępnego portu.

### 10.7 Konfiguracja środowiskowa

Jeśli będą potrzebne jakieś secrety środowiskowe, trzeba je będzie tutaj podać. Każdy template pack może oczekiwać zmiennych środowiskowych.

### 10.8 Wartości domyślne

Domyślnie może być wybrany pierwszy dostępny frontend, backend-db stack, dostępny port. Ścieżka do katalogu docelowego, nazwa projektu i zmienne środowiskowe muszą być podane.

## 11 Generation plan

### 11.1 Rola generation planu

Generation plan stanowić będzie listę kroków parametryzowanych do wykonania przez pipeline. Będzie utworzony na podstawie konfiguracji.
Efektem będzie źródło parametryzowanych kroków dla pipeline'u.

### 11.2 Wzór generation planu

- ścieżka do katalogu docelowego
- nazwa projektu
- frontend template pack
- backend-db stack template pack
- containerization template pack
- lista plików składanych z contributions

### 11.3 Utworzenie generation planu

Każdy z kroków będzie obiektem źródłowym dla wywołania odpowiedniego kroku pipeline'u.

## 12 Model kontraktów

### 12.1 Rola kontraktów w architekturze

Kontrakty pilnują, żeby poszczególne warstwy aplikacji były ze sobą kompatybilne i komunikowały się ze sobą. Wymuszają jeden określony sposób komunikacji.

### 12.2 Kontrakt HTTP API

Lista endpointów, których oczekuje frontend i które musi zagwarantować backend. Specyfikacja, jak każdy z nich ma wyglądać i zachowywać się. Specyfikacja błędów, jakich można od nich oczekiwać.

### 12.3 Kontrakt danych backend-db

Tabele domenowe, jakie muszą zawrzeć się w bazie danych oraz struktura ich kolumn i typów.

### 12.4 Zgodność template packów z kontraktami

Każdy dodany template pack musi spełniać te kontrakty, inaczej nie będzie kompatybilny z innymi.

### 12.5 Testowanie zgodności z kontraktami

Zawsze frontend posiada test happy path, który sprawdza podstawowy flow. Jeśli test nie przejdzie, kontrakt może nie być spełniony.

## 13 Template'y i template packi

### 13.1 Rola template'ów

Template to pojedynczy plik, będący częścią template packa, odwzorowywany na plik docelowy lub fragment pliku docelowego. Każdy template ma typ (częściowy, całościowy), treść oraz ścieżkę względną. Renderowanie templatu całościowego sprowadza się do jego skopiowania w odpowiednie miejsce, a częściowego do skopiowania jako contribution do pliku docelowego.

### 13.2 Rola template packów

Template pack składa się ze zbioru templatów całościowych, częściowych oraz manifestu.
Templaty całościowe są po prostu katalogiem do skopiowania.
Templaty częściowe zawierają treść oraz informację, do jakiego pliku kontrybuują.
Manifest określa rodzaj template packa, zależności, wersję.

### 13.3 Template pack jako jednostka rozszerzalności

Kiedy core zostanie ukończony, rozszerzanie generatora o kolejne wspierane frameworki będzie możliwe poprzez dodanie kolejnego template packa. Celem jest, aby nowa technologia nie wymagała zmiany czegokolwiek i jedynie wymagała dodanie nowego template packa.

### 13.4 Manifest template packa

Manifest zawiera wszystkie potrzebne informacje o template packu. To na podstawie manifestu zostaje dopasowany odpowiedni template pack.

Dane zawarte w manifeście (\* oznacza daną opcjonalną):

- Nazwa
- Rodzaj
- Wersja template packa
- \*Nazwa frameworka
- \*Wersja frameworka
- Język programowania
- Poziom stabilności {alfa, beta, stable}
- Lista zależności wymaganych przez template pack z zewnątrz
- Lista zależności, jakie template pack zainstaluje
- Zapotrzebowanie na zasoby
- Zapotrzebowanie na porty
- Dostarczane templaty częściowe

### 13.5 Ograniczenie logiki w template'ach

Template pack powinien być bazą modułu/frameworka/biblioteki napisanego zgodnie z najlepszymi, standardowymi dla niego praktykami. Powinien być stworzony w sposób natywny i łatwo rozszerzalny dla użytkownika.

### 13.6 Rodzaje template packów

#### 13.6.1 Frontend pack

Zawiera framework z frontendem. Jest wymagany do każdego projektu.

#### 13.6.2 Backend-db pack

Zawiera framework z backend-db stackiem. Jest wymagany do każdego projektu.

#### 13.6.3 Containerization pack

Zawiera konfigurację konteneryzacji. Jest wymagany.

#### 13.6.4 Infrastructure pack

Zawiera konfigurację związaną z infrastrukturą inną niż konteneryzacja. Serwer, ci/cd i tak dalej. Nie jest wymagany.

#### 13.6.5 Verification pack

Zawiera testy niezależne od użytego frameworka oraz procedury weryfikacji.

### 13.7 Wybór template packów

#### 13.7.1 Rejestr template packów

Rejestr jest tworzony podczas każdego wykonania programu. Wszystkie dostępne template packi znajdujące się w katalogu template_packs są sprawdzane, a dane pobierane z ich manifestów. Na tej podstawie następuje kategoryzacja.

#### 13.7.2 Dobór template packów

Żeby projekt zadziałał, muszą być odnalezione minimum cztery template packi, po jednym z każdej kategorii:

- Frontend
- Backend-db stack
- Konteneryzacja
- Verification

Inne nie są obowiązkowe, a projekt zadziała bez nich.

#### 13.7.3 Wykrywanie niewspieranych kombinacji

Każda kombinacja, jeśli została dodana, powinna być wspierana.
Dzięki temu, że każdy template pack ma swój typ, łatwo jest dobrać kompatybilny i pełny zbiór packów.

## 14 Rendering

### 14.1 Rola renderingu

Rendering to proces faktycznej generacji zawartości projektu. Pliki są kopiowane i składane w odpowiedni sposób, a wynikiem jest gotowy projekt.

### 14.2 Renderowanie plików właścicielskich

Pliki właścicielskie są bardzo proste do wyrenderowania. Wystarczy skopiować templaty całościowe do odpowiedniego katalogu.

### 14.3 Renderowanie plików składanych

Pliki składane tworzone są z templatów częściowych. Jeden z kroków pipeline'u tworzy wszystkie pliki składane i tworzy ich wspólny początek, a następnie dokleja części z kontrybuujących template packów.

### 14.4 Ograniczenie logiki w rendererze

Renderer jedynie kopiuje pliki lub skleja zawartość plików według prostego schematu. Dzięki temu nie ma ciężkiej logiki i jest stosunkowo mało podatny na błędy, a także niezależny od tego, co renderuje.

## 15 Verification

### 15.1 Rola verification

### 15.2 Verification jako krok pipeline'u zarządzany przez core

### 15.3 Verification wygenerowanego projektu

### 15.4 Verification kontraktu HTTP API

### 15.5 Verification kontraktu danych

### 15.6 Verification Docker Compose

### 15.7 Verification testów

### 15.8 Verification macierzy wspieranych kombinacji

### 15.9 Zachowanie po nieudanej verification

## 16 Statistics

### 16.1 Rola statystyk

### 16.2 Statystyki zbierane przez core

### 16.3 Statystyki kroków pipeline'u

### 16.4 Statystyki verification

### 16.5 Raport końcowy generacji

## 17 Struktura katalogów generatora

### 17.1 Proponowana struktura główna

### 17.2 Katalog core

### 17.3 Katalog contracts

### 17.4 Katalog template_packs

### 17.5 Katalog verification

### 17.6 Katalog tests

### 17.7 Katalog docs

## 18 Struktura wygenerowanego projektu

### 18.1 Struktura root projektu

### 18.2 Struktura frontendu

### 18.3 Struktura backendu

### 18.4 Pliki środowiskowe

### 18.5 Pliki Docker

### 18.6 README.md

### 18.7 Testy

## 19 Powiązanie architektury z kryteriami akceptacyjnymi

### 19.1 Kryteria generatora

### 19.2 Kryteria wspieranych kombinacji

### 19.3 Kryteria wygenerowanego projektu

### 19.4 Kryteria kontraktów

### 19.5 Kryteria idempotentności i wznawiania

### 19.6 Kryteria rozszerzalności

## 20 Elementy poza zakresem architektury
