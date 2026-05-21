from datetime import date

import todo_repository


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"all", "todo", "in_progress", "done", "open", "completed"}
VALID_TODO_STATUSES = {"todo", "in_progress", "done"}
TODO_FIELDS = {"title", "description", "completed", "status", "archived", "dueDate", "priority"}


class ValidationError(ValueError):
    pass


def validate_filters(status, priority, archived, due_date, due_before, due_after):
    if status not in VALID_STATUSES:
        raise ValidationError("Status must be one of: all, todo, in_progress, done.")
    if priority and priority not in VALID_PRIORITIES:
        raise ValidationError("Priority must be one of: low, medium, high.")
    if archived not in (None, "true", "false"):
        raise ValidationError("Archived must be true or false.")
    validate_date(due_date)
    validate_date(due_before)
    validate_date(due_after)


def validate_date(value):
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValidationError("Due date must be a string in YYYY-MM-DD format.")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError("Due date must use YYYY-MM-DD format.") from exc
    return value


def validate_todo_payload(data, require_title):
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object.")
    if not require_title and not TODO_FIELDS.intersection(data):
        raise ValidationError("At least one valid field is required.")

    cleaned = {}

    if require_title or "title" in data:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Title is required.")
        cleaned["title"] = title.strip()

    if "description" in data:
        description = data.get("description")
        if description is not None and not isinstance(description, str):
            raise ValidationError("Description must be a string.")
        cleaned["description"] = description.strip() if isinstance(description, str) else None

    if "completed" in data:
        completed = data.get("completed")
        if not isinstance(completed, bool):
            raise ValidationError("Completed must be a boolean.")
        cleaned["completed"] = completed
        cleaned["status"] = "done" if completed else "todo"

    if "status" in data:
        status = data.get("status")
        if status not in VALID_TODO_STATUSES:
            raise ValidationError("Status must be one of: todo, in_progress, done.")
        cleaned["status"] = status
        cleaned["completed"] = status == "done"

    if "archived" in data:
        archived = data.get("archived")
        if not isinstance(archived, bool):
            raise ValidationError("Archived must be a boolean.")
        cleaned["archived"] = archived

    if "dueDate" in data:
        cleaned["dueDate"] = validate_date(data.get("dueDate"))

    if "priority" in data:
        priority = data.get("priority") or "medium"
        if priority not in VALID_PRIORITIES:
            raise ValidationError("Priority must be one of: low, medium, high.")
        cleaned["priority"] = priority
    elif require_title:
        cleaned["priority"] = "medium"

    if require_title and "status" not in cleaned:
        cleaned["status"] = "todo"
        cleaned["completed"] = False
    if require_title and "archived" not in cleaned:
        cleaned["archived"] = False

    return cleaned


def list_todos(status="all", priority=None, query=None, archived="false", due_date=None, due_before=None, due_after=None):
    validate_filters(status, priority, archived, due_date, due_before, due_after)
    return todo_repository.find_all(
        status=status,
        priority=priority,
        query=query,
        archived=archived,
        due_date=due_date,
        due_before=due_before,
        due_after=due_after,
    )


def get_todo(todo_id):
    return todo_repository.find_by_id(todo_id)


def create_todo(payload):
    data = validate_todo_payload(payload, require_title=True)
    return todo_repository.insert(data)


def replace_todo(todo_id, payload):
    data = validate_todo_payload(payload, require_title=True)
    return todo_repository.replace(todo_id, data)


def patch_todo(todo_id, payload):
    if not payload:
        raise ValidationError("At least one field is required.")

    data = validate_todo_payload(payload, require_title=False)
    existing = todo_repository.find_by_id(todo_id)
    if existing is None:
        return None

    merged = {
        "title": data.get("title", existing["title"]),
        "description": data.get("description", existing["description"]),
        "completed": data.get("completed", existing["completed"]),
        "status": data.get("status", existing["status"]),
        "archived": data.get("archived", existing["archived"]),
        "dueDate": data.get("dueDate", existing["dueDate"]),
        "priority": data.get("priority", existing["priority"]),
    }
    return todo_repository.replace(todo_id, merged)


def delete_todo(todo_id):
    return todo_repository.delete(todo_id)


def get_statistics():
    return todo_repository.get_statistics()
