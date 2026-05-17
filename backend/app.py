from flask import Flask, jsonify
from flask_cors import CORS

from database import init_db
from routes import api


app = Flask(__name__)
CORS(app)
init_db()
app.register_blueprint(api)


def error_response(error, message, status_code):
    return jsonify({"error": error, "message": message}), status_code


@app.errorhandler(404)
def handle_route_not_found(error):
    return error_response("NotFound", "The requested route does not exist.", 404)


@app.errorhandler(500)
def handle_internal_error(error):
    return error_response("InternalServerError", "An unexpected server error occurred.", 500)


if __name__ == "__main__":
    app.run(debug=True)
