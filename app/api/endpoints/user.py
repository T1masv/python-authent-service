from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify

from app.api.endpoints import token_required
from app.api.schemas.user import DisplayUser
from app.dependencies import get_db

users_blueprint = Blueprint('users', __name__)


def filter_props(user):
    return {
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }


@users_blueprint.route('/users', methods=['GET'])
@token_required
def get_users(token, current_user, role):
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
def get_user(token, current_user,role , id):
    db = get_db()
    if role != 2:
        return jsonify({"status": "error", "message": "You are not authorized"}), 403

    user = db.users.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    filtered_user = filter_props(user)
    return jsonify({"status": "success", "user": filtered_user}), 200



@users_blueprint.route('/users/<id>', methods=['PUT'])
@token_required
def update_user(token, current_user, role, id):
    print(token, current_user, role, id)
    db = get_db()
    if role != 2:
        return jsonify({"status": "error", "message": "You are not authorized"}), 403

    user = db.users.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_data = request.get_json()
    db.users.update_one({"_id": ObjectId(id)}, {"$set": user_data})
    return jsonify({"status": "success", "message": "User successfully updated"}), 200


@users_blueprint.route('/users/<id>', methods=['DELETE'])
@token_required
def delete_user(token, current_user, role, id):
    print(token, current_user, role, id)

    db = get_db()
    if role != 2:
        return jsonify({"status": "error", "message": "You are not authorized"}), 403

    user = db.users.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    db.users.delete_one({"_id": ObjectId(id)})
    return jsonify({"status": "success", "message": "User successfully deleted"}), 200