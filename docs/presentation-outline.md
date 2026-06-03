# Presentation Outline

This outline follows the suggested course presentation structure. It can be used as the basis for the final presentation PDF.

## 1. Title Slide

Title:

```text
To-do List Management
```

Subtitle:

```text
API-first Web Application with Vue.js, Flask, SQLite, Tests, and nginx HTTPS Reverse Proxy
```

Include:

- Course name
- Team name or group number
- Team member names
- Presentation date

## 2. Ausgangssituation

Key message:

Many students and small project teams need a lightweight way to manage tasks, deadlines, and progress without using a large project management system.

Possible slide points:

- Tasks are often spread across notes, messages, or memory.
- A small web app is enough for simple task planning.
- The project is suitable for demonstrating frontend, backend, API, persistence, tests, and deployment.

## 3. Problemstellung

Key message:

The application should not only display tasks in the browser. It should provide a clean HTTP API, persist data, validate input, and keep business rules in the backend.

Possible slide points:

- Tasks need persistent storage.
- Users need CRUD operations.
- Status, archive state, due dates, filters, and statistics require backend logic.
- The API should also be usable without the frontend.

## 4. Zielsetzung

Key message:

Build a small but complete API-first web application with a clear architecture and a realistic deployment setup.

Goals:

- Vue.js SPA frontend with Vue Router
- Flask backend with REST API
- SQLite persistence
- OpenAPI contract
- Todo CRUD, filtering, status changes, archive support, and statistics
- Backend tests and coverage report
- nginx reverse proxy with HTTPS and HTTP-to-HTTPS redirect

## 5. Anforderungen / Use Cases

Use the user stories from `docs/project-concept.md`.

Suggested slide content:

| Use case | User value |
|---|---|
| Create todo | Store new work items |
| List and filter todos | Find relevant tasks quickly |
| Edit todo | Correct or update details |
| Change status | Track progress |
| Archive todo | Keep active list clean |
| View statistics | Understand task state quickly |
| Use HTTP API | Access data without frontend |

Short explanation:

The acceptance criteria are testable and map directly to API endpoints and frontend views.

## 6. HTTP API / OpenAPI

Key message:

The project follows an API-first approach. The API is described in `backend/openapi.yaml` and implemented by Flask routes.

Mention:

- Main resource: `Todo`
- JSON request and response bodies
- Consistent error format
- OpenAPI endpoint: `/api/openapi.yaml`

Important endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/todos` | List todos with filters |
| `POST` | `/api/todos` | Create todo |
| `GET` | `/api/todos/{id}` | Read one todo |
| `PUT` | `/api/todos/{id}` | Replace/update todo |
| `PATCH` | `/api/todos/{id}` | Partial update, status, archive |
| `DELETE` | `/api/todos/{id}` | Delete todo |
| `GET` | `/api/todos/stats` | Statistics |

## 7. Architektur der Webapplikation

Key message:

The project is a simple modular monolith with clear layers.

Architecture:

```text
Browser
  -> nginx HTTPS reverse proxy
  -> Vue.js static frontend
  -> /api requests proxied to Flask backend
  -> SQLite database
```

Layer mapping:

| Layer | Technology | Responsibility |
|---|---|---|
| Presentation | Vue.js, Bootstrap, Vue Router | UI, routing, user interaction |
| API | Flask routes | HTTP endpoints and responses |
| Business logic | todo_service.py | Validation, status/archive rules |
| Data | SQLite, repository module | Persistent storage |
| Deployment | Docker Compose, nginx | HTTPS entry point and proxy |

## 8. Backend-Implementierung

Key message:

The backend keeps business logic separate from routing and database access.

Important files:

| File | Responsibility |
|---|---|
| `backend/app.py` | Flask app setup |
| `backend/routes.py` | API routes |
| `backend/todo_service.py` | Validation and business logic |
| `backend/todo_repository.py` | SQLite CRUD queries |
| `backend/database.py` | Database connection and schema setup |

Business rules:

- Required title validation
- Allowed statuses: `todo`, `in_progress`, `done`
- `completed` and `status` stay consistent
- Archive state is persisted and filterable
- Due date format uses `YYYY-MM-DD`
- Statistics are calculated from SQLite data

## 9. Frontend-Implementierung

Key message:

The frontend is a Vue.js SPA that focuses on UI and API calls, while main business rules stay in the backend.

Important files:

| File | Responsibility |
|---|---|
| `frontend/src/router/index.js` | Vue Router routes |
| `frontend/src/services/todoApi.js` | Centralized fetch API calls |
| `frontend/src/views/TodoListView.vue` | List, filters, statistics, archive/delete |
| `frontend/src/views/TodoCreateView.vue` | Create form |
| `frontend/src/views/TodoDetailView.vue` | Detail and edit form |
| `frontend/src/App.vue` | Layout and navigation |

Mention:

- Bootstrap responsive grid and forms
- `onMounted()` loads API data in views
- `fetch()` with `async/await`
- Loading and error states

## 10. Tests and Coverage

Key message:

The backend is covered by integration tests and service-level tests.

Mention:

- API integration tests use Flask test client.
- Unit tests cover validation, status, archive, patch behavior, and statistics.
- Tests use an isolated temporary SQLite database.
- Coverage report is generated with `pytest-cov`.

Command:

```bash
cd backend
pytest --cov=. --cov-report=term-missing --cov-report=html
```

Current verified result:

```text
22 passed
Total coverage: 83%
```

## 11. Reverse Proxy and HTTPS

Key message:

nginx is the public entry point. It serves the Vue frontend over HTTPS and forwards API requests to Flask over HTTP inside Docker.

Mention:

- Docker Compose starts backend and nginx.
- HTTP port `80` redirects to HTTPS port `443`.
- Self-signed certificate is used for local development.
- `/api/` requests are proxied to `backend:5000`.
- Flask does not handle HTTPS directly.

Validation commands:

```bash
docker compose up --build
curl -I http://localhost
curl -k https://localhost/api/todos
curl -k https://localhost/api/todos/stats
```

## 12. Live-Demo

Use `docs/live-demo-guide.md` as the demo script.

Suggested demo order:

1. Open `https://localhost`.
2. Show the todo list and statistics.
3. Create a todo.
4. Change status to `in_progress` or `done`.
5. Filter by status and due date.
6. Archive and restore a todo.
7. Open one todo and edit details.
8. Show API call with `curl`.
9. Show HTTP-to-HTTPS redirect.

## 13. Herausforderungen / Lessons Learned

Possible points:

- Keeping frontend API calls clean with a separate service module.
- Keeping business logic out of the Vue components.
- Maintaining consistency between `completed` and `status`.
- Handling local HTTPS with a self-signed certificate.
- Using temporary SQLite databases for tests.
- Separating generated runtime files from Git.

## 14. Fazit und Ausblick

Conclusion:

The project fulfills the core course requirements with a complete API-first web application, persistent storage, tests, coverage reporting, and a realistic reverse proxy setup.

Possible future improvements:

- User accounts and authentication
- Pagination for long todo lists
- More detailed dashboard statistics
- CI pipeline for automated tests
- Deployment with a trusted certificate

## 15. Team Responsibilities

| Member | Part | Main responsibility | Presentation part |
|---|---|---|---|
| Fuqiang Zhang | A | Frontend, Vue Router, Bootstrap UI, Live-Demo operation | Frontend implementation and main UI demo |
| Jie Pan | B | Flask API, business logic, SQLite persistence | Backend, API endpoints, validation, and database |
| Leonard Lausen | C | Tests, OpenAPI, nginx reverse proxy, documentation | Testing, coverage, deployment, and conclusion |

Each team member should present a roughly equal amount of the project.
