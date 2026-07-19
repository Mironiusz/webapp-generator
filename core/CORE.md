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
- czy wybrane template packi deklarują wymagane kontrakty oraz czy nie powodują konfliktów plików, portów, zmiennych środowiskowych i contributions

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
