import os
from contextlib import contextmanager
from pathlib import Path
import sqlite3


DATABASE_PATH = Path(os.environ.get("TODO_DATABASE_PATH", Path(__file__).with_name("todos.db")))


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'todo',
                archived INTEGER NOT NULL DEFAULT 0,
                due_date TEXT,
                priority TEXT DEFAULT 'medium',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        ensure_column(connection, "status", "TEXT NOT NULL DEFAULT 'todo'")
        ensure_column(connection, "archived", "INTEGER NOT NULL DEFAULT 0")
        connection.execute(
            """
            UPDATE todos
            SET status = CASE WHEN completed = 1 THEN 'done' ELSE 'todo' END
            WHERE status IS NULL OR status = ''
            """
        )
        connection.execute(
            """
            UPDATE todos
            SET status = 'done'
            WHERE completed = 1 AND status = 'todo'
            """
        )


def ensure_column(connection, column_name, column_definition):
    columns = connection.execute("PRAGMA table_info(todos)").fetchall()
    existing_columns = {column["name"] for column in columns}
    if column_name not in existing_columns:
        connection.execute(f"ALTER TABLE todos ADD COLUMN {column_name} {column_definition}")
