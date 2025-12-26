from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.stats.service import stats_service

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")


@stats_bp.get("")
def get_stats():
    result = stats_service.get_all_stats()
    return {"success": True, "data": result}, 200


@stats_bp.route("/user/<int:user_id>", methods=["GET"])
def get_stats_by_user(user_id):
    result = stats_service.get_stats_by_user_id(user_id)
    return {"success": True, "data": result}, 200


@stats_bp.route("/summary/me", methods=["GET"])
@jwt_required()
def get_my_stats_summary():
    user_id = get_jwt_identity()
    result = stats_service.get_stats_summary_by_user_id(user_id)
    return {"success": True, "data": result}, 200


@stats_bp.route("/", methods=["POST"])
@jwt_required()
def create_stats():
    data = request.get_json() or {}
    data.setdefault("user_id", get_jwt_identity())
    try:
        result = stats_service.create_stats(data)
        return {"success": True, "data": result}, 201
    except ValueError as e:
        return {"success": False, "error": str(e)}, 400


@stats_bp.route("/<int:stats_id>", methods=["PUT"])
@jwt_required()
def update_stats(stats_id):
    data = request.get_json() or {}
    try:
        result = stats_service.update_stats(stats_id, data)
        return {"success": True, "data": result}, 200
    except ValueError as e:
        return {"success": False, "error": str(e)}, 400
