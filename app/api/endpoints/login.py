from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from app.api.endpoints import generate_token
from app.api.schemas.user import LoginUser
from app.dependencies import get_db

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    db = get_db()

    try:
        user_data = LoginUser(**request.get_json())
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400

    username = user_data.username
    password = user_data.password

    user_db = db.users.find_one({"username": username})
    if not user_db:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

    if check_password_hash(user_db['password'], password):
        return return_token(user_db['_id'])
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401


def return_token(user_id):
    # check if session exist
    db = get_db()
    token = generate_token(user_id)
    db.sessions.insert_one({"token": token})
    return jsonify({"status": "success", "token": token}), 201
