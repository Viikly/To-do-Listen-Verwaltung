# CODEX_UPDATE_ASSIGNMENT_3_4.md

## Purpose

This file is an incremental update for an existing project that was already generated from an earlier brief.

**Important:** Do not restart the project from scratch. Inspect the current repository first and update the existing implementation in place.

The project is for the course **Web-Technologien I** and implements a **To-do List Management** web application using an API-first approach.

---

## Current situation

An earlier version of the project may already exist. It may already contain some or all of the following:

- an OpenAPI description
- a backend implementation
- a simple data storage solution
- a frontend implementation
- a README

Before changing anything, inspect the current files and preserve useful existing work.

---

## Assignment 3 update: Backend implementation

The third assignment requires implementing the backend part of the project.

### Required backend framework

Use one of the following frameworks:

- Flask (Python)
- NestJS (JavaScript / TypeScript)

### Project decision

Use:

```text
Flask (Python)
```

Do not use Express.js.

### Backend task

Start implementing the **business logic** of the project.

Specifically:

1. Check whether an OpenAPI description already exists.
2. If it exists, use it as the contract for the implementation.
3. If it does not exist or is incomplete, create or complete `backend/openapi.yaml`.
4. Implement the REST endpoints specified in the OpenAPI description.
5. Add validation and reasonable error handling.
6. Add simple persistent data storage.

### Data storage

The assignment allows simple and freely chosen data storage, for example:

- SQLite
- MongoDB
- files

### Project decision

Use:

```text
SQLite
```

Reason: It is simple, persistent, easy to explain, and suitable for a small course project.

---

## Assignment 4 update: Vue.js frontend

The fourth assignment requires developing a **Single-Page Application (SPA) with Vue.js**.

### Required frontend technology

Use:

```text
Vue.js
```

The frontend should not remain a plain HTML/CSS/JavaScript page if that was created in an earlier version.

### Required frontend steps

1. Use Node.js and npm.
2. Create or update the frontend as a Vue.js project.
3. Prefer the official project setup command:

```bash
npm create vue@latest
```

4. Use the Vue Router to create multiple SPA routes.
5. Use `fetch()` or `axios` to retrieve data from the Flask API.
6. Put API communication into Vue components or into a small API service module.
7. Use the Vue lifecycle hook `onMounted()` to load data in the component that displays API data.

---

## Updated target technology stack

```text
API specification: OpenAPI 3.x, preferably backend/openapi.yaml
Backend: Flask (Python)
Database: SQLite
Frontend: Vue.js SPA
Frontend routing: Vue Router
API communication: fetch() or axios
Architecture: API-first, 3-layer architecture, modular monolith
```

---

## Architecture target

The project should be explainable as a simple 3-layer web application:

```text
Presentation layer: Vue.js SPA
Logic layer: Flask backend
Data layer: SQLite database
```

Do not build microservices. For this small course project, a modular monolith is sufficient and easier to explain.

---

## Recommended target project structure

The exact structure can differ if the existing project already has a reasonable structure, but the final project should be close to this:

```text
todo-api-first-project/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── todo_service.py
│   ├── todo_repository.py
│   ├── database.py
│   ├── openapi.yaml
│   ├── requirements.txt
│   └── todos.db
│
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── services/
│   │   │   └── todoApi.js
│   │   └── views/
│   │       ├── TodoListView.vue
│   │       ├── TodoCreateView.vue
│   │       ├── TodoDetailView.vue
│   │       └── AboutView.vue
│
└── README.md
```

---

## Required API endpoints

Use the OpenAPI file as the source of truth. For a To-do List project, the expected endpoints are usually:

```text
GET    /api/todos
GET    /api/todos/{id}
POST   /api/todos
PUT    /api/todos/{id}
PATCH  /api/todos/{id}
DELETE /api/todos/{id}
```

The implementation should match the OpenAPI specification. If the current OpenAPI file uses slightly different endpoint names, either follow the existing OpenAPI contract or update the contract consistently.

---

## Expected Todo data model

Use a simple Todo model such as:

```json
{
  "id": 1,
  "title": "Example task",
  "description": "Optional description",
  "completed": false,
  "dueDate": "2026-05-20",
  "priority": "medium",
  "createdAt": "2026-05-17T12:00:00Z",
  "updatedAt": "2026-05-17T12:00:00Z"
}
```

Minimum required fields:

```text
id
title
completed
createdAt
updatedAt
```

Optional but useful fields:

```text
description
dueDate
priority
```

---

## Vue.js SPA requirements

Implement several SPA views using Vue Router.

Recommended routes:

```text
/              redirect to /todos or show todo list
/todos         list all todos
/todos/new     create a new todo
/todos/:id     show detail and/or edit a todo
/about         show short project and architecture information
```

The Vue frontend should be able to:

1. Load all todos from the Flask API.
2. Show a loading state or simple error message.
3. Create a new todo.
4. Mark a todo as completed or not completed.
5. Edit an existing todo.
6. Delete a todo.
7. Navigate between views using Vue Router.

---

## API communication

Create a small API service module if possible, for example:

```text
frontend/src/services/todoApi.js
```

It should contain functions such as:

```text
getTodos()
getTodo(id)
createTodo(todo)
updateTodo(id, todo)
patchTodo(id, partialTodo)
deleteTodo(id)
```

Use either `fetch()` or `axios`.

---

## Validation after implementation

After making changes, validate the project.

### Backend checks

Run the Flask backend and test the endpoints.

Suggested manual checks:

```bash
curl http://localhost:5000/api/todos
```

Also test:

```text
POST /api/todos
GET /api/todos/{id}
PUT or PATCH /api/todos/{id}
DELETE /api/todos/{id}
```

### Frontend checks

Run the Vue frontend.

Suggested commands:

```bash
cd frontend
npm install
npm run dev
```

Check that:

1. The Vue app starts successfully.
2. The routes work.
3. The frontend can load todo data from the Flask backend.
4. Create, update, complete and delete operations work from the UI.

---

## README update

Update the README so that another student or teacher can run the project.

The README should include:

1. Project description
2. Technology stack
3. Architecture explanation
4. How to run the backend
5. How to run the frontend
6. API overview
7. Data storage explanation
8. Short note that the project follows the API-first approach with OpenAPI

Example sections:

```text
# To-do List Management

## Technology Stack
## Architecture
## API-first Approach
## Backend Setup
## Frontend Setup
## API Endpoints
## Database
```

---

## Development rules

1. Do not restart from scratch.
2. Preserve useful existing files.
3. Update the project incrementally.
4. Do not use Express.js.
5. Do not replace Flask with NestJS unless absolutely necessary.
6. Do not build microservices.
7. Do not remove OpenAPI.
8. Keep backend and frontend clearly separated.
9. Validate changes after implementation.
10. Commit changes in meaningful steps if Git is used.

---

## Priority order

Work in this order:

1. Inspect the existing repository.
2. Check whether the backend already uses Flask.
3. Check or create `backend/openapi.yaml`.
4. Implement or fix Flask endpoints according to OpenAPI.
5. Implement SQLite persistence.
6. Test backend endpoints.
7. Convert or replace the old frontend with a Vue.js SPA.
8. Add Vue Router routes.
9. Connect Vue components to the Flask API using `fetch()` or `axios`.
10. Test frontend-backend communication.
11. Update README.

---

## Short instruction prompt

If using this file with Codex, the user may say:

```text
Please read CODEX_UPDATE_ASSIGNMENT_3_4.md and update the existing project in place.
Do not restart from scratch.
Apply the third and fourth assignment requirements:
- Flask backend business logic and OpenAPI endpoints
- simple SQLite persistence
- Vue.js SPA frontend with Vue Router
- API calls via fetch() or axios, loaded in components with onMounted()

Validate the backend and frontend after implementation.
```
