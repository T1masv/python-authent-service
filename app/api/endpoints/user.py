from flask import Blueprint, jsonify
from app.dependencies import get_db
from app.api.endpoints import token_required, get_user_info
from bson.objectid import ObjectId

from app.api.schemas.user import DisplayUser

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
        users_db = list(db.users.find({}))
        print(users_db)
        users = [DisplayUser.parse_obj(_).dict() for _ in users_db]
        print(users)
    return jsonify({"status": "success", "users": users})


@users_blueprint.route('/users/<id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    db = get_db()
    if current_user['role'] != 2:
        return jsonify({"status": "error", "message": "You are not authorized"}), 403

    user = db.users.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    filtered_user = filter_props(user)
    return jsonify({"status": "success", "user": filtered_user}), 200


