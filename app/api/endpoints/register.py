from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.dependencies import get_db

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['POST'])
def register():
    db = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400

    # Check if user already exists
    if db.users.find_one({"username": username}):
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user document
    new_user = {
        "username": username,
        "password": hashed_password
    }

    # Insert new user into the database
    db.users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201
