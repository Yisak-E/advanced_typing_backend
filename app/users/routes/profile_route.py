from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.service.user_profile_service import (
    get_profile_by_user_id,
    update_profile,
    get_all_profiles,
)

profile_bp = Blueprint("profiles", __name__, url_prefix="/profiles")


@profile_bp.get("")
def get_profiles():
    profiles = get_all_profiles()
    return jsonify({"success": True, "data": {"profiles": profiles}}), 200


@profile_bp.get("/me")
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()
    profile = get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"success": False, "error": "Profile not found"}), 404
    return jsonify({"success": True, "data": profile.serialize()}), 200


@profile_bp.put("/me")
@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    try:
        profile = update_profile(user_id, data)
        return jsonify({"success": True, "data": profile.serialize()}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@profile_bp.route("/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    profile = get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"success": False, "error": "Profile not found"}), 404
    if profile.profile_visibility == "private":
        return jsonify({"success": False, "error": "Profile is private"}), 403
    return jsonify({"success": True, "data": profile.serialize()}), 200
