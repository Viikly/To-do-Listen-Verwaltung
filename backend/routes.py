from flask import Blueprint, current_app, jsonify, request, send_from_directory

import todo_service
from todo_service import ValidationError


api = Blueprint("api", __name__)


def error_response(error, message, status_code):
    return jsonify({"error": error, "message": message}), status_code


@api.get("/")
def root():
    return jsonify(
        {
            "name": "Todo API",
            "status": "running",
            "message": "Use /api/todos to access the Todo API.",
        }
    )


@api.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@api.get("/api/openapi.yaml")
def openapi_spec():
    return send_from_directory(current_app.root_path, "openapi.yaml", mimetype="text/yaml")


@api.get("/api/todos")
def get_todos():
    try:
        todos = todo_service.list_todos(
            status=request.args.get("status", "all"),
            priority=request.args.get("priority"),
            query=request.args.get("q"),
            archived=request.args.get("archived", "false"),
            due_date=request.args.get("dueDate"),
            due_before=request.args.get("dueBefore"),
            due_after=request.args.get("dueAfter"),
        )
    except ValidationError as exc:
        return error_response("ValidationError", str(exc), 400)

    return jsonify(todos)


@api.get("/api/todos/stats")
def get_todo_stats():
    return jsonify(todo_service.get_statistics())


@api.get("/api/todos/<int:todo_id>")
def get_todo(todo_id):
    todo = todo_service.get_todo(todo_id)
    if todo is None:
        return error_response("NotFound", "Todo does not exist.", 404)
    return jsonify(todo)


@api.post("/api/todos")
def post_todo():
    try:
        todo = todo_service.create_todo(request.get_json(silent=True))
    except ValidationError as exc:
        return error_response("ValidationError", str(exc), 400)

    return jsonify(todo), 201


@api.put("/api/todos/<int:todo_id>")
def put_todo(todo_id):
    try:
        todo = todo_service.replace_todo(todo_id, request.get_json(silent=True))
    except ValidationError as exc:
        return error_response("ValidationError", str(exc), 400)

    if todo is None:
        return error_response("NotFound", "Todo does not exist.", 404)
    return jsonify(todo)


@api.patch("/api/todos/<int:todo_id>")
def patch_existing_todo(todo_id):
    try:
        todo = todo_service.patch_todo(todo_id, request.get_json(silent=True))
    except ValidationError as exc:
        return error_response("ValidationError", str(exc), 400)

    if todo is None:
        return error_response("NotFound", "Todo does not exist.", 404)
    return jsonify(todo)


@api.delete("/api/todos/<int:todo_id>")
def delete_existing_todo(todo_id):
    deleted = todo_service.delete_todo(todo_id)
    if not deleted:
        return error_response("NotFound", "Todo does not exist.", 404)
    return "", 204
