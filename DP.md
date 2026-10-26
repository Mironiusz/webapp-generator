# SDI - Duża Prezentacja

## Tytuł

Generator Szkieletów Aplikacji Webowych

Rafał Mironko, Informatyka, Inżynieria Oprogramowania

Opiekun: Szymon Kijas, IAiIS

## Plan prezentacji (1min)

- Omówienie problemu
- Cel pracy i efekt dla użytkownika
- Opis oczekiwanego działania
- Funkcjonalność bazowa
- Funkcjonalność produkcyjna
- Funkcjonalność techniczna
- Potencjalne rozszerzenia
- Kluczowe decyzje projektowe i założenia architekroniczne
- Ryzyka projektowe
- Weryfikacja
- Specyfikacja
- Architektura
- Dotychczasowe wyniki pracy
- Plan prac na ten semestr

## Omówienie problemu (2min)

Wielu programistów doskonale potrafi rozszerzać i edytować aplikację webową. Gorzej, kiedy trzeba postawić nową - nikt tego nie lubi, a mało kto potrafi bez przypomnienia sobie w dokumentacji poprawnie uruchomić instalator Vite, napisać podstawowy routing, zainstalować odpowiednie pakiety, połączyć frontend z backendem bez problemów z CORS i stworzyć Dockerfile, który od razu zadziała. Do tego, nieważne jak dobry programista by nie był, to wszystko po prostu zabiera czas.
Dlatego właśnie postanowiłem stworzyć generator aplikacji webowych, który wszystkie te nieprzyjemne boilerplate'owe kroki wykona za użytkownika.

## Cel pracy (2min)

Celem projektu jest zaprojektowanie i implementacja narzędzia CLI generującego konteneryzowane szkielety aplikacji webowych na podstawie kreatora lub pliku konfiguracyjnego. Generator ma ograniczyć ilość powtarzalnej pracy potrzebnej do uruchomienia nowej aplikacji oraz zapewnić spójny, testowalny i rozszerzalny punkt startowy dla dalszego rozwoju projektu.

Po przejściu przez kreator aplikacji lub uruchomieniu generatora z plikiem konfiguracyjnym powstaje działający, konteneryzowany szkielet aplikacji webowej z konfiguracją środowiskową, który wystarczy rozszerzać i modyfikować.

## Opis oczekiwanego działania

- użytkownik uruchamia kreator albo wskazuje plik konfiguracyjny
- wybiera lub deklaruje frontend (Vue, React)
- wybiera lub deklaruje backend-db stack (FastAPI + SQLite, Django + PostgreSQL)

Następnie generator tworzy gotowy projekt.

## Specyfikacja

Specyfikacja określa, co generator ma robić oraz jakie warunki musi spełniać wygenerowany projekt, ale nie narzuca sposobu implementacji wewnętrznej generatora.

### Zakres specyfikacji

Specyfikacja obejmuje:

- działanie generatora
- format danych wejściowych
- wymagany wynik generacji
- minimalne wymagania wobec wygenerowanej aplikacji
- kontrakt API
- kontrakt danych
- testy
- wymagania niefunkcjonalne

### Tryby działania

1. Tryb kreatora

Użytkownik odpowiada na pytania i podejmuje decyzje:

- nazwa projektu
- ścieżka docelowa
- frontend
- backend-db stack
- porty albo wartości domyślne
- dane środowiskowe albo wartości domyślne

2. Tryb pliku konfiguracyjnego

Generator przyjmuje plik konfiguracyjny i działa bez jakiejkolwiek interakcji

### Wspierane technologie i kombinacje

Na początku zakładałem:

Generator musi wspierać następujące kombinacje:

- Nuxt + FastAPI + SQLite
- React + FastAPI + SQLite
- Nuxt + Django + PostgreSQL
- React + Django + PostgreSQL

Generator w tej wersji nie musi obsługiwać kombinacji spoza tej listy, ale musi być rozszerzalny o nowe frameworki frontendowe i backendowe.

Jednak przez brak czasu prawdopodobnie zrezygnuję z Reacta, oraz przez przesyt Pythonem być może zmienię Django na ASP.NET Core + PostgreSQL.

### Wymagania funkcjonalne generatora

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

### Wymagania funkcjonalne wygenerowanej aplikacji

1. Frontend

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

2. Backend

- endpoint health, db i ready
- endpoint login
- endpoint register
- endpoint zwracający dane aktualnego użytkownika
- obsługa CORS
- obsługa JWT
- testy jednostkowe
- testy integracyjne

3. Baza danych

Baza danych jest w PostgreSQL lub w SQLite.

Backend zapewnia:

- migracje
- minimalny model użytkownika
- strukturę danych wymaganą do działania podstawowego mechanizmu uwierzytelniania

4. Komunikacja

- działa komunikacja frontend-backend
- działa komunikacja backend-db

"Działanie" definiuję przejściem testów e2e.

### Kontrakt danych

Minimalny model użytkownika musi pozwalać na:

- jednoznaczną identyfikację użytkownika
- logowanie za pomocą emaila
- rejestrację za pomocą emaila
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

Kontrakt danych nie wymaga identycznej fizycznej struktury wszystkich tabel dla każdego backendu. Backend może posiadać dodatkowe tabele techniczne wymagane przez framework.

### Wymagania niefunkcjonalne

1. Idempotentność

Ponowne uruchomienie generatora dla tej samej konfiguracji nie może prowadzić do niespójnego lub częściowo uszkodzonego projektu.

2. Deterministyczność

Dla tej samej konfiguracji generator powinien tworzyć taki sam wynik strukturalny.

3. Rozszerzalność

Dodanie nowego frontendu albo backendu nie powinno wymagać modyfikacji istniejących wspieranych kombinacji technologicznych.

4. Niezależność wygenerowanego projektu od generatora

Wygenerowany projekt musi być możliwy do uruchomienia bez generatora.

5. Jakość wygenerowanego projektu

Wygenerowany projekt musi spełniać szeroko pojęte dobre praktyki programistyczne, między innymi:

- zasady SOLID
- zasada DRY
- testy jednostkowe dla kluczowych elementów backendu i frontendu
- testy integracyjne potwierdzające działającą komunikację frontend-backend oraz backend-db
- samodokumentujący się, czytelny kod z docstringami funkcji, ale bez komentarzy linijkowych
- pliki dokumentacyjne informujące, jak rozszerzać moduły i zgodnie z jakimi standardami zostały one stworzone

Projekt ma być łatwy do rozszerzenia dla użytkownika generatora, bez konieczności tworzenia zupełnie nowych modułów i wprowadzania nowych standardów.

## Kluczowe decyzje projektowe i założenia architekroniczne

1. Frontend zależy wyłącznie od kontraktu HTTP API
   Frontend nie wie nic o tym, jaki backend został wybrany. Dla frontendu istotne jest jedynie to, żeby backend wystawiał mu określone endpointy. Dzięki temu, rozszerzanie generatora o wsparcie dla dowolnych frontendów jest bardzo proste - ponieważ frontend pełni rolę warstwy prezentacji oraz klienta korzystającego z publicznego API backendu.

2. Backend i baza danych traktowane są jako backend-db stack
   Być może na papierze wygodne byłoby rozdzielenie backendu i bazy danych, żeby tworzyć dowolne kombinacje. Niestety, backend ma zbyt duży wpływ na sposób działania bazy danych:
   - ORM
   - migracje
   - modele
   - auth
   - struktura danych wymagana do uwierzytelniania
   - tabele techniczne
   - testy backend-db

   To wszystko sprawia, że obsługa takiej macierzy kombinacji szybko stałaby się nienatywna i pełna sztucznych warunków. Stąd decyzja o utrzymaniu backendu i bazy danych jako jednego backend-db stacka.

3. Baza danych wynika z wybranego backend-db stacka

   Jest to świadome ograniczenie zakresu pracy. Użytkownik nie będzie mógł w podstawowej wersji dowolnie łączyć backendu z bazą danych. Jego decyzją będzie wybór jednego ze wspieranych backend-db stacków: FastAPI + SQLite albo Django + PostgreSQL. Dodanie większej liczby obsługiwanych stacków nie powinno wymagać zmiany założeń architektonicznych, ale zwiększyłoby ilość pracy implementacyjnej, testowej i dokumentacyjnej oraz spowodowałoby konieczność dodawania kolejnych stacków jeden po drugim. Dlatego podstawowa wersja pracy zawiera tylko stacki wskazane w specyfikacji.

4. Kontrakty zamiast jakichkolwiek adapterów

   Ta zasada chroni wygenerowany projekt przed sztuczną warstwą abstrakcji, jaką byłby dowolny adapter. Nie chcę, żeby projekt miał dodatkowe adaptery tylko dlatego, że generator obsłuży inne kombinacje. Dzięki temu spójność i natywność wygenerowanego kodu zostanie osiągnięta przez kontrakty:
   - Frontend jest kompatybilny z backendem, bo spełniają kontrakt API,
   - Backend-db stack jest zgodny z wymaganiami projektu, bo spełnia kontrakt danych.

5. Natywność template packów

   Template pack będzie generował kod, który jest naturalny dla danej technologii. Django nie zostanie wciśnięte w typową strukturę FastAPI, a Nuxt nie będzie udawać Reacta. Dlatego kluczowe będzie dokładne zapoznanie się ze wzorcami standardowymi dla obsługiwanych technologii, a następnie utworzenie każdego template packa zgodnie z nimi. Przykład konwencji:
   - Django -> Django ORM, migracje Django, struktura Django
   - FastAPI -> struktura FastAPI, osobna konfiguracja aplikacji, osobne modele/schemy
   - Nuxt -> routing oparty na plikach, struktura typowa dla Nuxta
   - React -> React Router, Vite, struktura typowa dla Reacta

   Jeśli wspólne będą jedynie wymagania, a nie struktura kodu, osiągniemy naturalny projekt, pozbawiony złych nawyków lub wymuszeń związanych z innymi frameworkami.

6. Wygenerowany projekt nie zależy runtime'owo od generatora

   Generator jest jedynie narzędziem do tworzenia projektu, a nie jego częścią. Projekt po skopiowaniu do katalogu docelowego ma funkcjonować bez generatora. Wygenerowany projekt nie powinien importować bibliotek generatora ani wymagać go do uruchamiania, testowania lub dalszego rozwijania.

7. Kontrolowane powtórzenia zamiast sztucznych abstrakcji

   W zwykłym projekcie często dąży się do DRY. W wypadku generatora zbyt agresywne DRY mogłoby jednak sprawić, że ucierpią na tym generowane projekty. Współdzielenie jednej abstrakcji między różnymi frameworkami skończyłoby się strukturą nienaturalną dla żadnego z nich. Z tego powodu akceptuję pewne powtórzenia, jeśli są konieczne, żeby:
   - template pack pozostał natywny
   - wygenerowany kod pozostał czytelny
   - framework działał zgodnie z typowymi dla siebie konwencjami
   - nowa technologia nie wymagała modyfikowania starej

   Dlatego wygenerowane projekty powinny być możliwie DRY, ale sam generator może świadomie zawierać kontrolowane powtórzenia w template packach.

## Ryzyka projektowe

- największe ryzyka projektu mają charakter architektoniczny, ponieważ błędne decyzje dotyczące kontraktów, template packów lub pipeline'u mogą utrudnić dalsze rozszerzanie generatora
- zbyt duża liczba kombinacji technologicznych sprawi, że mogę nie zdążyć stworzyć pracy
- zbyt mała liczba kombinacji technologicznych może nie dać pewności, że dodawanie kolejnych nie wymaga modyfikacji istniejących
- ponieważ podstawowy zakres obejmuje wyłącznie backendy z ekosystemu Pythona, projekt w ograniczonym stopniu weryfikuje i testuje możliwość dodania backendu z innego języka programowania, np. Node.js, Java lub C#, mimo że z perspektywy architektonicznej powinno to być możliwe
- zbyt agresywne stosowanie zasady DRY może prowadzić do sztucznych abstrakcji między technologiami. W projekcie ważniejsze jest zachowanie natywności template packów oraz zgodność z zasadą open/closed, nawet kosztem kontrolowanego powtórzenia części kodu lub konfiguracji

## Architektura

### Przepływ i główne etapy działania

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
   Generator waliduje konfigurację i sprawdza, czy jest ona obsługiwana. Sprawdza, czy porty nie mają konfliktów oraz czy da się stworzyć output_dir.

4. Stworzenie planu generacji
   Plan generacji jest zbiorem danych parametryzujących generację projektu. Zostanie on przekazany do pipeline'u. Plan generacji powinien wykryć konflikty między packami - na przykład jeśli chcą wyrenderować ten sam plik. Odróżnia renderowanie pliku od składania go z kilku packów, informuje, jakie pliki składane zostaną stworzone.

5. Generowanie w katalogu roboczym
   Generator nie zaczyna od katalogu docelowego, ale robi staging. Na podstawie stałej listy kroków oraz planu generacji zostaje przeprowadzony cały proces - renderowanie template'ów, tworzenie struktury katalogów, zapis plików i przygotowanie konteneryzacji.

6. Weryfikacja
   Etap sprawdzenia, czy wygenerowany projekt rzeczywiście spełnia wymagania. Jest to główne odróżnienie tego generatora od prostego kopiowania template'ów. Poprawność projektu nie jest oceniana tym, że pliki powstały, tylko tym, że przechodzą wymagane testy.
   Weryfikacja sprawdza, czy Docker Compose uruchamia wymagane kontenery, backend odpowiada na GET /health, backend komunikuje się z bazą, frontend komunikuje się z backendem, wszystkie testy przechodzą oraz happy path rejestracji, logowania i pobrania danych aktualnego użytkownika działa.

7. Finalizacja
   Ostatni etap, przenoszący zweryfikowany projekt do docelowego katalogu. Jeśli weryfikacja nie zakończy się sukcesem, projekt nie zostaje przeniesiony do katalogu docelowego.

### Podział systemu na główne części

1. Core

Core jest głównym modułem sterującym generatora. Core nie może znać szczegółów frameworków, z jakich korzysta. Musi on orkiestrować cały proces generacji:

- uruchomienie CLI
- wczytanie danych
- normalizacja konfiguracji
- walidacja konfuguracji
- planning
- zarządzanie wykonaniem kroków pipeline'u
- zapis i odczyt stanu generacji
- obsługa błędów
- przekazanie wyniku do outputu
- zebranie statystyk

Dzięki temu, w przypadku rozszerzania o kolejne technologie, core nie powinien wymagać istotnych modyfikacji.

2. Pipeline

Zarządzany przez core iterowalny proces, przechodzący przez renderowanie, weryfikację i output. Pipeline umożliwia przechodzenie ze stanu do stanu w przód, a informacje o artefaktach i efektach ubocznych kroków pozwalają core'owi wykonać cleanup albo wznowienie procesu.

3. Template packs

Część systemu, która dostarcza kod i konfigurację dla konkretnych technologii. Template packi znają szczegóły frameworków, mieści się w nich docelowa struktura generowanego kodu.
Template packi powinny być możliwie niezależne od siebie i komunikować się przez kontrakty oraz contributions. Jeśli autor chce rozszerzyć generator o obsługę kolejnej technologii, po prostu dodaje kolejny template pack. To tam mieści się cały kod, konfiguracja, obsługa kontraktów. Dzięki temu, wystarczy w zasadzie dobrze znać wybrany framework, żeby móc utworzyć dla niego template pack.
Istnieją różne rodzaje template packów. Template pack zawiera pełne templaty plików oraz templaty contributions, gdzie docelowy plik powstaje ze wszystkich kontrybuujących do niego templatów.

4. Planning

Część odpowiedzialna za przetłumaczenie konfiguracji na plan generacji. Na tym etapie konfiguracja zostaje zamieniona na zestaw template packów, contributions i danych potrzebnych do renderowania. Dzięki niemu proces jest przewidywalny i deterministyczny oraz gwarantuje poprawny plan.

5. Rendering

Proces zmieniający templaty wybrane w planie generacji na realne pliki w katalogu. Renderer przyjmuje template packi i renderuje pełne pliki oraz pliki składane z contributions.

6. Output

Output odpowiada za fizyczny zapis wyniku, zarówno do stagingu, jak i do katalogu docelowego. Pilnuje też, żeby wynikowa struktura nie była uszkodzona.

Zadania outputu:

- zapewnienie pustego katalogu roboczego
- zapis plików
- przeniesienie projektu do docelowego katalogu
- czyszczenie po błędzie zgodnie z decyzją core
- ochrona docelowego katalogu przed uszkodzonym wynikiem

7. State

Zapisany stan działania generatora. Bezpieczne korzystanie ze stanów jest możliwe, ponieważ zakładamy, że wynik dla każdej konfiguracji jest deterministyczny. Dzięki temu, core może łatwo wstrzymać i przywrócić proces, obsłużyć błąd w jednym z kroków i powtórzyć krok bez konieczności powtarzania całego procesu generacji oraz łatwo wyczyścić stan i rozpocząć od nowa. Stan pozwala wykryć, czy konfiguracja została zmieniona. Jeśli hash konfiguracji nie zgadza się ze stanem zapisanym z poprzedniego przebiegu, core nie wznawia działania, tylko czyści stan i rozpoczyna proces od nowa.

8. Verification

Weryfikacja sprawdza, czy projekt w stagingu działa poprawnie. Wygenerowany projekt, zanim trafi do folderu docelowego, jest dokładnie sprawdzany w folderze stagingu. Dzięki temu nie wprowadzamy niedziałającego projektu do katalogu docelowego. Weryfikacja jest wykonywana jako jeden lub kilka kroków pipeline'u zarządzanego przez core.

9. Statistics

Część odpowiedzialna za mierzenie i raportowanie przebiegu generacji. Statystyki zbierają:

- czas całej generacji
- czas poszczególnych etapów
- wybraną kombinację technologiczną
- liczbę wygenerowanych plików
- liczbę użytych template packów
- status verification
- informację o błędzie, jeśli wystąpił

Mogą też służyć do porównywania czasu trwania etapów oraz czasu generacji różnych kombinacji technologicznych.

## Dotychczasowe wyniki pracy (5min)

### Dokumentacje

- dokumentacja wstępna (117)
- specyfikacja (522)
- kryteria akceptacyjne (586)
- architektura (1001)

### Template packi

- przygotowana infra dla wszystkich packów opartych na Pythonie
- utworzony template pack FastAPI + SQLite

### Generator

- przygotowana infra dla generatora
- ustrukturyzowanie i zaplanowanie całej pracy
- ukończony moduł konfiguracji

## Plan prac na ten semestr + programin minimum (2min)

### Faza 2

- implementacja core: CLI, wykonanie planu generacji, obsługa pipelinu
- implementacja kroków pipelinu
- określenie formatu planu generacji, implementacja
- implementacja renderera i outputu, procedura weryfikacji i finalizacji

### Faza 3

- template pack Nuxta

### Faza 4

- dokończenie generatora

### Faza 5

- napisanie pracy inżynierskiej w docelowym formacie

### Faza 6

- dodanie template packa React i ASP.Net

## Slajd końcowy

- powtórzenie slajdu tytułowego
