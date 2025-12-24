from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.service.user_profile_service import (
    get_profile_by_user_id,
    update_profile
)

profile_bp = Blueprint("profiles", __name__, url_prefix="/profiles")


@profile_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()

    profile = get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(profile.serialize()), 200


@profile_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    profile = update_profile(user_id, data)

    return jsonify(profile.serialize()), 200
