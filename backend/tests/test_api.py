def create_todo(client, **overrides):
    payload = {
        "title": "Write API tests",
        "description": "Cover the Flask endpoints",
        "status": "todo",
        "archived": False,
        "dueDate": "2026-06-01",
        "priority": "medium",
    }
    payload.update(overrides)
    return client.post("/api/todos", json=payload)


def test_create_todo(client):
    response = create_todo(client, title="Create test", status="in_progress")

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] > 0
    assert data["title"] == "Create test"
    assert data["status"] == "in_progress"
    assert data["completed"] is False
    assert data["archived"] is False


def test_list_todos(client):
    create_todo(client, title="First todo")
    create_todo(client, title="Second todo")

    response = client.get("/api/todos")

    assert response.status_code == 200
    titles = {todo["title"] for todo in response.get_json()}
    assert {"First todo", "Second todo"} <= titles


def test_get_single_todo(client):
    created = create_todo(client, title="Single todo").get_json()

    response = client.get(f"/api/todos/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Single todo"


def test_update_todo(client):
    created = create_todo(client, title="Before update").get_json()

    response = client.put(
        f"/api/todos/{created['id']}",
        json={
            "title": "After update",
            "description": None,
            "status": "done",
            "archived": False,
            "dueDate": None,
            "priority": "high",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "After update"
    assert data["status"] == "done"
    assert data["completed"] is True
    assert data["priority"] == "high"


def test_patch_status(client):
    created = create_todo(client, status="todo").get_json()

    response = client.patch(f"/api/todos/{created['id']}", json={"status": "in_progress"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "in_progress"
    assert data["completed"] is False


def test_archive_todo(client):
    created = create_todo(client).get_json()

    response = client.patch(f"/api/todos/{created['id']}", json={"archived": True})

    assert response.status_code == 200
    assert response.get_json()["archived"] is True


def test_filter_by_status(client):
    create_todo(client, title="Todo item", status="todo")
    create_todo(client, title="Progress item", status="in_progress")

    response = client.get("/api/todos?status=in_progress")

    assert response.status_code == 200
    todos = response.get_json()
    assert [todo["title"] for todo in todos] == ["Progress item"]


def test_filter_by_archived(client):
    create_todo(client, title="Active item", archived=False)
    archived = create_todo(client, title="Archived item", archived=True).get_json()

    response = client.get("/api/todos?archived=true")

    assert response.status_code == 200
    todos = response.get_json()
    assert len(todos) == 1
    assert todos[0]["id"] == archived["id"]


def test_filter_by_due_date(client):
    create_todo(client, title="Due target", dueDate="2026-06-01")
    create_todo(client, title="Other date", dueDate="2026-07-01")

    response = client.get("/api/todos?dueDate=2026-06-01")

    assert response.status_code == 200
    todos = response.get_json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Due target"


def test_get_statistics(client):
    create_todo(client, status="todo")
    create_todo(client, status="in_progress")
    create_todo(client, status="done")
    create_todo(client, archived=True)

    response = client.get("/api/todos/stats")

    assert response.status_code == 200
    stats = response.get_json()
    assert stats["total"] == 4
    assert stats["active"] == 3
    assert stats["archived"] == 1
    assert stats["todo"] == 1
    assert stats["inProgress"] == 1
    assert stats["done"] == 1


def test_validation_error(client):
    response = client.post("/api/todos", json={"title": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "ValidationError"


def test_not_found_error(client):
    response = client.get("/api/todos/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "NotFound"


def test_delete_todo(client):
    created = create_todo(client).get_json()

    delete_response = client.delete(f"/api/todos/{created['id']}")
    get_response = client.get(f"/api/todos/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
