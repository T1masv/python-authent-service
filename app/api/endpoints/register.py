from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.dependencies import get_db
from app.api.schemas.user import RegisterUser
from pydantic import ValidationError

register_blueprint = Blueprint('register', __name__)


@register_blueprint.route('/register', methods=['POST'])
def register():
    db = get_db()

    try:
        user_data = RegisterUser(**request.get_json())
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400



    # Check if user already exists
    if db.users.find_one({"username": user_data.username}):
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

    # Hash the password
    hashed_password: str = generate_password_hash(user_data.password)
    user_data.password = hashed_password

    # Insert new user into the database
    db.users.insert_one(user_data.dict())

    return jsonify({'message': 'User registered successfully', "status": "success"}), 201
