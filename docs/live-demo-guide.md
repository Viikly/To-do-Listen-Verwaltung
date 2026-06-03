# Live Demo Guide

This guide describes a short and reproducible demo flow for the final project presentation.

## Demo Goal

Show that the application is a complete API-first web application:

- Vue.js SPA frontend
- Flask REST API
- SQLite persistence
- CRUD operations
- Status, archive, filters, and statistics
- OpenAPI documentation
- Backend tests with coverage
- nginx HTTPS reverse proxy

## Before the Demo

Start from a clean terminal in the project root:

```powershell
cd E:\HSBI资料\Web\To-do
```

Check Git status if needed:

```bash
git status --short --branch
```

Make sure Docker Desktop is running.

Generate the local certificate if it does not exist:

```powershell
$env:OPENSSL_CONF='NUL'
openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
  -keyout nginx/certs/localhost.key `
  -out nginx/certs/localhost.crt `
  -subj "/C=DE/ST=NRW/L=Bielefeld/O=WebTech/OU=Development/CN=localhost"
```

Start the application:

```bash
docker compose up --build
```

If another terminal is preferred:

```bash
docker compose up --build -d
```

## Technical Validation Before Presenting

Check running containers:

```bash
docker compose ps
```

Check HTTP-to-HTTPS redirect:

```bash
curl -I http://localhost
```

Expected result:

```text
HTTP/1.1 301 Moved Permanently
Location: https://localhost/
```

Check API through nginx:

```bash
curl -k https://localhost/api/todos
curl -k https://localhost/api/todos/stats
```

Check backend tests and coverage:

```bash
cd backend
pytest --cov=. --cov-report=term-missing --cov-report=html
```

Expected verified result:

```text
22 passed
TOTAL coverage: 83%
```

## Demo Script

Suggested presenter handoff:

| Presenter | Part | Demo responsibility |
|---|---|---|
| Fuqiang Zhang | A | Open the app, explain Vue SPA, routes, responsive UI, and operate the frontend demo |
| Jie Pan | B | Explain Flask API, business logic, SQLite persistence, CRUD, status, archive, filters, and statistics |
| Leonard Lausen | C | Explain OpenAPI, tests, coverage, nginx HTTPS reverse proxy, and final validation commands |

### 1. Open the Application

Open:

```text
https://localhost
```

The browser will show a certificate warning because the certificate is self-signed. Accept the warning for the local demo.

Explain:

- nginx is serving the Vue frontend over HTTPS.
- The frontend uses relative `/api` requests.
- nginx forwards `/api/` requests to the Flask backend.

### 2. Show the Start View

Show:

- Navigation bar
- Todo list page
- Statistics cards
- Filter controls
- Create/edit navigation

Explain:

- This is a Vue.js SPA.
- Routing is handled by Vue Router.
- Data is loaded in components with `onMounted()`.

### 3. Create a Todo

Go to:

```text
/todos/new
```

Create an example todo:

| Field | Example |
|---|---|
| Title | Prepare live demo |
| Description | Show API, frontend, tests, and nginx |
| Due date | 2026-06-15 |
| Priority | High |
| Status | In progress |

Expected result:

- The app redirects back to the list.
- The new todo appears in the list.
- Statistics update.

Explain:

- Frontend sends `POST /api/todos`.
- Backend validates the payload.
- SQLite stores the todo.

### 4. Change Status

Use the checkbox or edit page to mark a todo as done.

Expected result:

- Status changes to `done`.
- `completed` becomes `true`.
- Statistics update.

Explain:

- `PATCH /api/todos/{id}` updates only selected fields.
- The service layer keeps `status` and `completed` consistent.

### 5. Filter Todos

Try these filters in the UI:

- Status: `In progress`
- Status: `Done`
- Archive: `Active todos`
- Due date or due date range
- Search text

Expected result:

- The list updates based on backend query parameters.

Explain:

- Filters are sent as query parameters to `GET /api/todos`.
- Filtering is done in the backend repository query.

### 6. Archive and Restore

Archive a todo from the list.

Expected result:

- The todo disappears from active todos.
- The archived count changes.

Switch archive filter to:

```text
Archived todos
```

Restore the todo.

Explain:

- Archive is not a delete.
- The todo remains in SQLite with `archived = true`.

### 7. Edit a Todo

Open the edit/detail view.

Change:

- Description
- Priority
- Due date
- Status

Expected result:

- Changes are saved.
- The updated todo is shown in the list.

Explain:

- `GET /api/todos/{id}` loads details.
- `PUT /api/todos/{id}` replaces the todo with validated data.

### 8. Show API Access Without Frontend

Run:

```bash
curl -k https://localhost/api/todos
```

Optionally create a todo through the API:

```bash
curl -k -X POST https://localhost/api/todos ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Created through curl\",\"status\":\"todo\",\"priority\":\"medium\"}"
```

PowerShell alternative:

```powershell
curl.exe -k -X POST https://localhost/api/todos `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"Created through curl\",\"status\":\"todo\",\"priority\":\"medium\"}"
```

Explain:

- The API is not only for the frontend.
- Script clients can use it directly.

### 9. Show OpenAPI

Open or request:

```text
https://localhost/api/openapi.yaml
```

Explain:

- This is the API contract.
- It documents endpoints, schemas, request bodies, responses, and errors.

### 10. Show Tests and Coverage

Run:

```bash
cd backend
pytest --cov=. --cov-report=term-missing --cov-report=html
```

Open the HTML report if needed:

```text
backend/coverage/html/index.html
```

Explain:

- API integration tests use the Flask test client.
- Business logic tests cover validation and todo rules.
- Tests use a temporary SQLite database and do not modify `backend/todos.db`.

## Demo Cleanup

If Docker was started in detached mode:

```bash
docker compose down
```

If you want to remove the Docker volume and demo data:

```bash
docker compose down -v
```

Use `-v` only when demo data should be deleted.

## Backup Demo Plan

If Docker has a problem:

1. Start backend locally:

```bash
cd backend
python app.py
```

2. Start frontend locally in another terminal:

```bash
cd frontend
npm run dev
```

3. Open:

```text
http://127.0.0.1:5173
```

This fallback does not demonstrate nginx HTTPS, but it still demonstrates the core frontend, backend, API, SQLite, and tests.
