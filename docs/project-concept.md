# Project Concept

This document summarizes the project requirements, user stories, acceptance criteria, and API concept for the To-do List Management application.

## Project Goal

The application helps users manage personal or study-related tasks in a simple web interface. It uses an API-first structure with a Vue.js SPA frontend, a Flask backend, SQLite persistence, and an nginx HTTPS reverse proxy for deployment.

The main goal is not only to store todos, but also to demonstrate a clear web application architecture:

- Frontend: presentation layer, user interaction, API calls
- Backend: HTTP API, validation, business logic
- Database: persistent todo storage
- Reverse proxy: HTTPS entry point and request forwarding

## User Stories

### US-01: Create Todo

Als Benutzer moechte ich eine neue Aufgabe erstellen, um wichtige Arbeitsschritte festzuhalten.

Acceptance criteria:

- A user can enter a title.
- A title is required and cannot be empty.
- A user can optionally enter a description, priority, status, and due date.
- After creation, the todo is stored in SQLite.
- The created todo is visible in the todo list.
- Invalid input returns a clear validation error.

Related API endpoint:

```text
POST /api/todos
```

### US-02: List Todos

Als Benutzer moechte ich alle aktiven Aufgaben sehen, um einen Ueberblick ueber meine Arbeit zu bekommen.

Acceptance criteria:

- The todo list loads data from the backend API.
- Active todos are shown by default.
- Each todo shows title, status, priority, due date, and archive state.
- Loading and error states are visible in the frontend.
- The API can also be called by an external script client.

Related API endpoint:

```text
GET /api/todos
```

### US-03: View and Edit Todo

Als Benutzer moechte ich eine einzelne Aufgabe ansehen und bearbeiten, um Details nachtraeglich zu korrigieren.

Acceptance criteria:

- A user can open a detail page for one todo.
- The frontend loads the todo by ID.
- A user can update title, description, priority, status, due date, and archive state.
- If the todo does not exist, the backend returns a `404` error.
- Invalid updates return a `400` validation error.

Related API endpoints:

```text
GET /api/todos/{id}
PUT /api/todos/{id}
PATCH /api/todos/{id}
```

### US-04: Change Status

Als Benutzer moechte ich den Bearbeitungsstatus einer Aufgabe setzen, um den Fortschritt sichtbar zu machen.

Acceptance criteria:

- A todo can have one of these statuses: `todo`, `in_progress`, `done`.
- The frontend can change a status through the API.
- If `status` is set to `done`, the backend also marks `completed` as `true`.
- If `completed` is changed directly, the backend keeps `status` consistent.
- Invalid status values are rejected.

Related API endpoint:

```text
PATCH /api/todos/{id}
```

### US-05: Archive Todo

Als Benutzer moechte ich erledigte oder nicht mehr relevante Aufgaben archivieren, um die aktive Liste uebersichtlich zu halten.

Acceptance criteria:

- A todo can be archived through the frontend.
- Archived todos are hidden from the active list by default.
- A user can switch the archive filter to view archived todos.
- A todo can be restored from the archive.
- The archive state is persisted in SQLite.

Related API endpoints:

```text
PATCH /api/todos/{id}
GET /api/todos?archived=true
GET /api/todos?archived=false
```

### US-06: Filter Todos

Als Benutzer moechte ich Aufgaben filtern und suchen, um relevante Aufgaben schneller zu finden.

Acceptance criteria:

- A user can filter by status.
- A user can filter by archive state.
- A user can filter by exact due date.
- A user can filter by due date range.
- A user can search text in title and description.
- Invalid filter values return a validation error.

Related API endpoint:

```text
GET /api/todos?status=in_progress&archived=false&dueBefore=2026-06-30
```

### US-07: See Statistics

Als Benutzer moechte ich einfache Statistiken sehen, um den Gesamtzustand meiner Aufgaben schnell einzuschaetzen.

Acceptance criteria:

- The frontend shows statistics cards.
- The backend returns counts for total, active, archived, todo, in progress, done, and overdue todos.
- Statistics are calculated from persisted data.
- Archived todos are counted separately from active status statistics.

Related API endpoint:

```text
GET /api/todos/stats
```

### US-08: Use the API as External Client

Als API-Client moechte ich Aufgaben ueber HTTP verwalten, um die Anwendung auch ohne Frontend benutzen zu koennen.

Acceptance criteria:

- The API is documented with OpenAPI.
- Requests and responses use JSON.
- CRUD operations are available through stable REST endpoints.
- Error responses use a consistent JSON structure.
- The API is reachable through nginx at `/api/`.

Related files:

```text
backend/openapi.yaml
nginx/nginx.conf
```

## API-Konzept

### API-First Approach

The API contract is described in `backend/openapi.yaml`. The backend routes implement this contract, and the Vue frontend consumes the API instead of storing the main todo data locally.

The API is designed around one main resource:

```text
Todo
```

Supporting endpoints provide health checks, OpenAPI documentation, and statistics.

### Base URLs

Local backend development:

```text
http://localhost:5000
```

Docker/nginx deployment:

```text
https://localhost
```

### Resource: Todo

A todo represents one task.

Important fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | integer | Unique todo ID |
| `title` | string | Required task title |
| `description` | string or null | Optional task details |
| `completed` | boolean | Compatibility flag for completed state |
| `status` | string | Workflow status: `todo`, `in_progress`, `done` |
| `archived` | boolean | Whether the todo is hidden from the active list |
| `dueDate` | string or null | Optional due date in `YYYY-MM-DD` format |
| `priority` | string | `low`, `medium`, or `high` |
| `createdAt` | string | Creation timestamp |
| `updatedAt` | string | Last update timestamp |

### Endpoint Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API welcome response |
| `GET` | `/api/health` | Backend health check |
| `GET` | `/api/openapi.yaml` | OpenAPI description |
| `GET` | `/api/todos` | List todos with optional filters |
| `POST` | `/api/todos` | Create a todo |
| `GET` | `/api/todos/stats` | Get todo statistics |
| `GET` | `/api/todos/{id}` | Get one todo |
| `PUT` | `/api/todos/{id}` | Replace/update a todo |
| `PATCH` | `/api/todos/{id}` | Partially update a todo |
| `DELETE` | `/api/todos/{id}` | Delete a todo |

### Query Parameters

`GET /api/todos` supports these filters:

| Parameter | Example | Meaning |
|---|---|---|
| `status` | `in_progress` | Filter by workflow status |
| `archived` | `false` | Show active or archived todos |
| `priority` | `high` | Filter by priority |
| `dueDate` | `2026-06-15` | Match exact due date |
| `dueBefore` | `2026-06-30` | Todos due on or before a date |
| `dueAfter` | `2026-06-01` | Todos due on or after a date |
| `q` | `project` | Search in title and description |

### Request Examples

Create a todo:

```json
{
  "title": "Prepare presentation",
  "description": "Explain API, backend, frontend, tests, and nginx setup",
  "status": "in_progress",
  "priority": "high",
  "dueDate": "2026-06-15"
}
```

Patch status:

```json
{
  "status": "done"
}
```

Archive a todo:

```json
{
  "archived": true
}
```

### Response Examples

Todo response:

```json
{
  "id": 1,
  "title": "Prepare presentation",
  "description": "Explain API, backend, frontend, tests, and nginx setup",
  "completed": false,
  "status": "in_progress",
  "archived": false,
  "dueDate": "2026-06-15",
  "priority": "high",
  "createdAt": "2026-06-03T12:00:00Z",
  "updatedAt": "2026-06-03T12:00:00Z"
}
```

Statistics response:

```json
{
  "total": 8,
  "active": 6,
  "archived": 2,
  "todo": 3,
  "inProgress": 2,
  "done": 1,
  "overdue": 1
}
```

Error response:

```json
{
  "error": "ValidationError",
  "message": "Title is required."
}
```

### HTTP Status Codes

| Status code | Meaning |
|---|---|
| `200` | Successful read or update |
| `201` | Todo created |
| `204` | Todo deleted |
| `400` | Validation error |
| `404` | Todo not found |
| `500` | Unexpected backend error |

### Business Logic Rules

The backend service layer is responsible for these rules:

- `title` is required for create and replace operations.
- `status` must be `todo`, `in_progress`, or `done`.
- `archived` must be a boolean in request bodies.
- `dueDate`, `dueBefore`, and `dueAfter` must use `YYYY-MM-DD`.
- `completed` and `status` are kept consistent.
- Statistics are calculated from persisted SQLite data.

### Architecture Mapping

| Layer | Files | Responsibility |
|---|---|---|
| Presentation | `frontend/src/views`, `frontend/src/router` | UI, routing, lifecycle loading, user feedback |
| API | `backend/routes.py` | HTTP endpoints and response mapping |
| Business logic | `backend/todo_service.py` | Validation, status/archive rules, statistics access |
| Data | `backend/todo_repository.py`, `backend/database.py` | SQLite queries, persistence, schema setup |
| Deployment | `docker-compose.yml`, `nginx/nginx.conf` | HTTPS entry point, reverse proxy, Docker services |

### Validation and Testing

The API is covered by integration tests using the Flask test client. The business logic is covered by unit tests for validation, status handling, archive behavior, patch behavior, and statistics calculation.

Coverage can be generated with:

```bash
cd backend
pytest --cov=. --cov-report=term-missing --cov-report=html
```
