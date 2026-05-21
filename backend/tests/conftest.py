import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture()
def test_database(tmp_path, monkeypatch):
    import database

    test_db_path = tmp_path / "todos_test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_db_path)
    database.init_db()
    return test_db_path


@pytest.fixture()
def client(test_database):
    import app as app_module

    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client
