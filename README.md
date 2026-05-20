# To-do List Management

This project is an API-first web application for managing to-do tasks. It was built for Web-Technologien I and demonstrates a small 3-layer architecture with a Vue.js SPA frontend, a Flask backend, and SQLite persistence.

## Technology Stack

- API specification: OpenAPI 3.0 in `backend/openapi.yaml`
- Backend: Flask with Python
- Database: SQLite
- Frontend: Vue.js 3 SPA
- Frontend routing: Vue Router
- API communication: `fetch()`

## Architecture

The project is a simple modular monolith with three clear layers:

```text
Presentation layer: Vue.js SPA
Logic layer: Flask routes and todo service
Data layer: SQLite database through a repository module
```

The backend is split into:

- `routes.py`: HTTP endpoints and response mapping
- `todo_service.py`: validation and business logic
- `todo_repository.py`: SQLite CRUD operations
- `database.py`: connection and table initialization

## API-first Approach

The API contract is documented in `backend/openapi.yaml`. The Flask routes implement the endpoints described there, and the Vue frontend calls the REST API instead of storing the main data locally.

When the backend is running, the OpenAPI file is also available at:

```text
http://localhost:5000/api/openapi.yaml
```

## Project Structure

```text
.
backend/
  app.py
  routes.py
  todo_service.py
  todo_repository.py
  database.py
  openapi.yaml
  requirements.txt
frontend/
  package.json
  vite.config.js
  index.html
  src/
    main.js
    App.vue
    router/
    services/
    views/
    assets/
.gitignore
README.md
```

## Backend Setup

Create and activate a virtual environment:

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The backend runs at:

```text
http://localhost:5000
```

## Frontend Setup

Install dependencies and start the Vue development server:

```bash
cd frontend
npm install
npm run dev
```

The frontend usually runs at:

```text
http://127.0.0.1:5173
```

The Vue app uses these routes:

| Route | Purpose |
|---|---|
| `/` | Redirects to `/todos` |
| `/todos` | List, filter, complete, and delete todos |
| `/todos/new` | Create a new todo |
| `/todos/:id` | View and edit one todo |
| `/about` | Project and architecture information |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/openapi.yaml` | OpenAPI document |
| `GET` | `/api/todos` | Read all todos |
| `GET` | `/api/todos/{id}` | Read one todo |
| `POST` | `/api/todos` | Create a todo |
| `PUT` | `/api/todos/{id}` | Replace/update a todo |
| `PATCH` | `/api/todos/{id}` | Partially update a todo |
| `DELETE` | `/api/todos/{id}` | Delete a todo |

Optional filters for `GET /api/todos`:

```text
?status=all
?status=open
?status=completed
?priority=high
?q=project
```

## Database

SQLite is used for simple persistence. The backend creates the `todos` table automatically when the app starts. The generated local database file is:

```text
backend/todos.db
```

This file is ignored by Git because it is local runtime data.

## Example Request

```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Check OpenAPI\",\"priority\":\"high\",\"dueDate\":\"2026-05-20\"}"
```
