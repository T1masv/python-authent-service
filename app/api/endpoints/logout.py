from flask import Blueprint, jsonify

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route('/logout', methods=['POST'])
def logout():
    # Implementation of logout logic
    return jsonify({"status": "success", "message": "Logged out successfully"})
