from flask import Blueprint, jsonify
from app.dependencies import get_db
from app.api.endpoints import token_required, get_user_info

users_blueprint = Blueprint('users', __name__)


def filter_props(user):
    return {
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }


@users_blueprint.route('/users', methods=['GET'])
@token_required
def get_users(current_user, role):
    db = get_db()

    if role != 2:
        return jsonify({"status": "error", "message": "You are not authorized"})
    else:
        users = [filter_props(_) for _ in db.users.find()]
    return jsonify({"status": "success", "users": users})
