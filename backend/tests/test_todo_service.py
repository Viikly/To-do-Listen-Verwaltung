import pytest

import todo_service


def test_required_title_validation():
    with pytest.raises(todo_service.ValidationError, match="Title is required"):
        todo_service.validate_todo_payload({"title": "   "}, require_title=True)


@pytest.mark.parametrize("status", ["todo", "in_progress", "done"])
def test_valid_status_values(status):
    payload = todo_service.validate_todo_payload(
        {"title": "Status test", "status": status},
        require_title=True,
    )

    assert payload["status"] == status
    assert payload["completed"] is (status == "done")


def test_invalid_status_value():
    with pytest.raises(todo_service.ValidationError, match="Status must be one of"):
        todo_service.validate_todo_payload(
            {"title": "Status test", "status": "blocked"},
            require_title=True,
        )


def test_archive_payload_validation():
    payload = todo_service.validate_todo_payload(
        {"title": "Archive test", "archived": True},
        require_title=True,
    )

    assert payload["archived"] is True


def test_archive_requires_boolean():
    with pytest.raises(todo_service.ValidationError, match="Archived must be a boolean"):
        todo_service.validate_todo_payload(
            {"title": "Archive test", "archived": "yes"},
            require_title=True,
        )


def test_patch_update_behavior(test_database):
    created = todo_service.create_todo(
        {
            "title": "Patch me",
            "description": "Before",
            "status": "todo",
            "dueDate": "2026-06-01",
            "priority": "medium",
        }
    )

    updated = todo_service.patch_todo(
        created["id"],
        {"status": "done", "archived": True},
    )

    assert updated["title"] == "Patch me"
    assert updated["description"] == "Before"
    assert updated["status"] == "done"
    assert updated["completed"] is True
    assert updated["archived"] is True


def test_statistics_calculation(test_database):
    todo_service.create_todo({"title": "Todo", "status": "todo"})
    todo_service.create_todo({"title": "Progress", "status": "in_progress"})
    todo_service.create_todo({"title": "Done", "status": "done"})
    todo_service.create_todo({"title": "Archived", "archived": True})

    stats = todo_service.get_statistics()

    assert stats["total"] == 4
    assert stats["active"] == 3
    assert stats["archived"] == 1
    assert stats["todo"] == 1
    assert stats["inProgress"] == 1
    assert stats["done"] == 1
