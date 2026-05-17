from datetime import datetime, timezone

from database import get_connection


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def row_to_todo(row):
    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "dueDate": row["due_date"],
        "priority": row["priority"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def find_all(status="all", priority=None, query=None):
    sql = "SELECT * FROM todos WHERE 1 = 1"
    params = []

    if status == "open":
        sql += " AND completed = 0"
    elif status == "completed":
        sql += " AND completed = 1"

    if priority:
        sql += " AND priority = ?"
        params.append(priority)

    if query:
        sql += " AND (LOWER(title) LIKE ? OR LOWER(COALESCE(description, '')) LIKE ?)"
        search = f"%{query.lower()}%"
        params.extend([search, search])

    sql += " ORDER BY completed ASC, due_date IS NULL ASC, due_date ASC, created_at DESC"

    with get_connection() as connection:
        rows = connection.execute(sql, params).fetchall()
    return [row_to_todo(row) for row in rows]


def find_by_id(todo_id):
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    return row_to_todo(row)


def insert(data):
    timestamp = now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO todos (title, description, completed, due_date, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["title"],
                data.get("description"),
                int(data.get("completed", False)),
                data.get("dueDate"),
                data.get("priority", "medium"),
                timestamp,
                timestamp,
            ),
        )
        todo_id = cursor.lastrowid
    return find_by_id(todo_id)


def replace(todo_id, data):
    timestamp = now_iso()
    with get_connection() as connection:
        result = connection.execute(
            """
            UPDATE todos
            SET title = ?, description = ?, completed = ?, due_date = ?, priority = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                data["title"],
                data.get("description"),
                int(data.get("completed", False)),
                data.get("dueDate"),
                data.get("priority", "medium"),
                timestamp,
                todo_id,
            ),
        )
        if result.rowcount == 0:
            return None
    return find_by_id(todo_id)


def delete(todo_id):
    with get_connection() as connection:
        result = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    return result.rowcount > 0
