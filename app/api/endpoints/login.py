from flask import Blueprint, request, jsonify
from app.dependencies import get_db
from werkzeug.security import check_password_hash

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400

    user_db = db.users.find_one({"username":username})
    if not user_db:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

    if check_password_hash(user_db['password'], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"status": "error","message": "Invalid username or password"}), 401
