from flask import Blueprint, jsonify

from app.api.endpoints import token_required
from app.dependencies import get_db

logout_blueprint = Blueprint('logout', __name__)


@logout_blueprint.route('/logout', methods=['DELETE'])
@token_required
def logout(token, current_user, role):
    # Implementation of logout logic
    db = get_db()
    db.sessions.delete_one({"token": token})
    return jsonify({"status": "success", "message": "Logged out successfully"})
