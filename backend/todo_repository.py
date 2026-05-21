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
        "status": row["status"],
        "archived": bool(row["archived"]),
        "dueDate": row["due_date"],
        "priority": row["priority"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def find_all(status="all", priority=None, query=None, archived="false", due_date=None, due_before=None, due_after=None):
    sql = "SELECT * FROM todos WHERE 1 = 1"
    params = []

    if status == "open":
        sql += " AND status != 'done'"
    elif status == "completed":
        sql += " AND status = 'done'"
    elif status != "all":
        sql += " AND status = ?"
        params.append(status)

    if archived == "true":
        sql += " AND archived = 1"
    elif archived == "false":
        sql += " AND archived = 0"

    if priority:
        sql += " AND priority = ?"
        params.append(priority)

    if due_date:
        sql += " AND due_date = ?"
        params.append(due_date)
    if due_before:
        sql += " AND due_date IS NOT NULL AND due_date <= ?"
        params.append(due_before)
    if due_after:
        sql += " AND due_date IS NOT NULL AND due_date >= ?"
        params.append(due_after)

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
            INSERT INTO todos (title, description, completed, status, archived, due_date, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["title"],
                data.get("description"),
                int(data.get("completed", False)),
                data.get("status", "todo"),
                int(data.get("archived", False)),
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
            SET title = ?, description = ?, completed = ?, status = ?, archived = ?, due_date = ?, priority = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                data["title"],
                data.get("description"),
                int(data.get("completed", False)),
                data.get("status", "todo"),
                int(data.get("archived", False)),
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


def get_statistics():
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN archived = 0 THEN 1 ELSE 0 END) AS active,
                SUM(CASE WHEN archived = 1 THEN 1 ELSE 0 END) AS archived,
                SUM(CASE WHEN archived = 0 AND status = 'todo' THEN 1 ELSE 0 END) AS todo,
                SUM(CASE WHEN archived = 0 AND status = 'in_progress' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN archived = 0 AND status = 'done' THEN 1 ELSE 0 END) AS done,
                SUM(CASE WHEN archived = 0 AND status != 'done' AND due_date IS NOT NULL AND due_date < DATE('now') THEN 1 ELSE 0 END) AS overdue
            FROM todos
            """
        ).fetchone()

    return {
        "total": row["total"] or 0,
        "active": row["active"] or 0,
        "archived": row["archived"] or 0,
        "todo": row["todo"] or 0,
        "inProgress": row["in_progress"] or 0,
        "done": row["done"] or 0,
        "overdue": row["overdue"] or 0,
    }
