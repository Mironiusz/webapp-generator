# FastAPI Backend

## Co to jest

Ten backend służy jako baza do rozwoju jako dowolna aplikacja. Zawiera podstawowe endpointy i logikę użytkownika, które są konieczne do stworzenia jakiejkolwiek zaawansowanej aplikacji.

Zapewnia:

- jednoznaczną identyfikację użytkownika
- logowanie za pomocą emaila
- rejestrację za pomocą emaila
- weryfikację hasła zapisanego jako hash
- oznaczenie użytkownika jako aktywnego lub nieaktywnego

## Stack

- FastAPI i Uvicorn
- SQLAlchemy 2 async, SQLite przez aiosqlite
- Alembic do migracji
- Pydantic i pydantic-settings do walidacji i konfiguracji
- PyJWT (HS256) do tokenów, pwdlib z Argon2 do hashowania
- pytest, ruff, mypy strict

## Uruchomienie

Backend działa w kontenerach Dockera uruchamianych Docker Compose. Compose samo ustawia ścieżki bazy i logów oraz wykonuje migracje przed startem backendu.

### Wymagania

- Docker Engine 25 lub nowszy, Docker Compose v2
- wolny port `8000` na hoście

### Pliki env

Utworz envy z plików .env.example:

```bash
cp .env.example .env
cp .env.local.example .env.local
```

W `.env` ustaw swój `AUTH__SECRET_KEY`. Klucz musi mieć co najmniej 32 znaki. Nie zostawiaj klucza z `.env.example`, bo jest na publicznym repo.

Generacja nowego `AUTH__SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Start

```bash
docker compose up -d --build
```

Docker najpierw uruchomi migrację, a potem postawi backend. Jeśli migracja nie powiedzie się, backend nie wstanie, a log znajdziesz w `docker compose logs migrate`.

Stan usług sprawdzisz poleceniem:

```bash
docker compose ps -a
```

Poprawny wynik to `migrate` w stanie `Exited (0)` i `backend` w stanie `Up (healthy)`.

### Szybkie sprawdzenie

Najwygodniej sprawdzić backend Swaggerem. Żeby to zrobić, do linka kontenera (domyślnie `http://127.0.0.1:8000/`) dopisz `/docs`:

```link
http://127.0.0.1:8000/docs#/
```

Sprawdzenie może wyglądać tak:

1. `GET /health/ready` zwraca 200 i `schema_status` jest `ready`.
2. Wywołaj `POST /api/v1/auth/register`, a potem `POST /api/v1/auth/login` z tym samym emailem i hasłem.
3. Skopiuj z response `access_token`, kliknij Authorize i wklej sam token, bez przedrostka `Bearer`.
4. `GET /api/v1/auth/me` zwraca zarejestrowanego użytkownika.

### Zatrzymanie i dane

```bash
docker compose down
```

Baza leży w wolumenie `backend-data` i przeżyje `docker compose down` oraz `docker compose up -d --build`. Żeby została usunięta, trzeba wywołać `docker compose down -v`.

## Konfiguracja

Konfigurację wczytuje `app/core/config.py`. W kontenerze trafia do niej zawartość plików `.env` i `.env.local` przekazana przez compose.

- `.env` przechowuje sekrety, a `.env.local` pozostałe ustawienia potencjalnie różne dla różnych maszyn. Oba pliki są w `.gitignore`.
- Pola zagnieżdżone rozdziela `__`, np. `AUTH__SECRET_KEY` trafia do `settings.auth.secret_key`.
- Listy podaje się jako JSON, np. `API__CORS_ORIGINS='["http://localhost:3000"]'`.
- Ścieżki bazy i logu w kontenerze ustawia `docker-compose.yml`. Wartości `DATABASE__URL` i `LOG__FILE_PATH` z plików env nie mają na nie wpływu.

Najważniejsze zmienne:

| Zmienna                    | Domyślnie      | Opis                                            |
| -------------------------- | -------------- | ----------------------------------------------- |
| `AUTH__SECRET_KEY`         | brak, wymagana | klucz podpisu tokenów JWT, co najmniej 32 znaki |
| `AUTH__ALGORITHM`          | `HS256`        | algorytm podpisu tokenów                        |
| `AUTH__TOKEN_LIFETIME_MIN` | `60`           | czas życia tokena w minutach                    |
| `ENVIRONMENT`              | `local`        | `local` albo `production`                       |
| `API__CORS_ORIGINS`        | `["*"]`        | originy, z których przeglądarka może wołać API  |
| `DATABASE__ECHO`           | `false`        | czy wypisywać zapytania SQL do logów            |

## Testy i komendy developerskie

### Docker

| Komenda                          | Co robi                                             |
| -------------------------------- | --------------------------------------------------- |
| `docker compose up -d --build`   | buduje obraz, wykonuje migracje i uruchamia backend |
| `docker compose ps -a`           | pokazuje stan usług, także zakończonej `migrate`    |
| `docker compose logs -f backend` | śledzi log backendu                                 |
| `docker compose down`            | zatrzymuje i usuwa kontenery, baza zostaje          |
| `docker compose down -v`         | zatrzymuje kontenery i usuwa bazę                   |

### Testy i narzędzia jakości

Obraz zawiera tylko zależności potrzebne do działania aplikacji, więc testów, lintów i typechecków tam nie będzie - trzeba uruchomić je lokalnie na hoście.

Potrzebujesz Pythona 3.13 i make. Utwórz środowisko wirtualne poleceniem `python -m venv venv` i aktywuj je:

- Git Bash: `source venv/Scripts/activate`
- PowerShell: `venv\Scripts\Activate.ps1`
- Linux i macOS: `source venv/bin/activate`

Następnie:

```bash
make install
make check
```

Spis komend `make`:

| Komenda          | Co robi                                                               |
| ---------------- | --------------------------------------------------------------------- |
| `make install`   | instaluje projekt w trybie edytowalnym z zależnościami deweloperskimi |
| `make lint`      | sprawdza kod i formatowanie ruffem                                    |
| `make format`    | formatuje kod i poprawia to, co ruff umie poprawić sam                |
| `make typecheck` | uruchamia mypy                                                        |
| `make test`      | uruchamia pytest                                                      |
| `make check`     | lint, typecheck i testy razem                                         |
