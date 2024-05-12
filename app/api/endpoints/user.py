from flask import Blueprint, jsonify
from app.dependencies import get_db

logout_blueprint = Blueprint('users', __name__)

@logout_blueprint.route('/users', methods=['GET'])
def get_users():
    db = get_db()

    # chek authent


    return jsonify({"status": "success", "message": "Logged out successfully"})
