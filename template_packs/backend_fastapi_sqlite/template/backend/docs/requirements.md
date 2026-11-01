## Decyzje stack

- FastAPI
- SQLAlchemy
- Alembic
- SQLite

## SQLite

- int autoincrement
- migracje z Alembic

## Kontrakty

## Endpointy

### 10.1 GET /health

Endpoint służy do sprawdzenia, czy backend działa.

### 10.2 POST /auth/register

Endpoint służy do utworzenia konta użytkownika.

### 10.3 POST /auth/login

Endpoint służy do zalogowania użytkownika i zwrócenia tokena JWT.

### 10.4 GET /auth/me

Endpoint służy do pobrania danych aktualnie zalogowanego użytkownika na podstawie tokena JWT.

## 10.5 PATCH /users/{id}

Endpoint służy do aktywowania, dezaktywowania i usuwania użytkownika

## 10.6 DELETE /users/{id}

Endpoint służy do usunięcia uzytkownika.

## Bezpieczeństwo
