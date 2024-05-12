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

    username = user_data.username
    password = user_data.password
    role = user_data.role.value
    email = user_data.email

    # Check if user already exists
    if db.users.find_one({"username": username}):
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user document
    new_user = {
        "username": username,
        "password": hashed_password,
        "role": role,
        "email": email
    }

    # Insert new user into the database
    db.users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully', "status": "success"}), 201
