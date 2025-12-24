from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.stats.service.stats_service import get_all_stats, get_stats_by_user_id

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")

@stats_bp.route("/", methods=["GET"])
def get_stats():
    try:
        result = get_all_stats()
        return {
            "success": True,
            "data": result
        }, 200
    except Exception as e:
        raise e


@stats_bp.route("/user/<int:user_id>", methods=["GET"])
def get_stats_by_user(user_id):
    try:
        result = get_stats_by_user_id(user_id)
        return {
            "success": True,
            "data": result
        }, 200
    except Exception as e:
        raise e

@stats_bp.route("/<int:stats_id>", methods=["GET"])
def get_stats_by_id(stats_id):
    try:
        result = get_stats_by_id(stats_id)
        return {
            "success": True,
            "data": result
        }, 200
    except Exception as e:
        raise e

@stats_bp.route("/", methods=["POST"])
def create_stats():
    try:
        data = request.get_json() or {}
        result = create_stats(data)
        return {
            "success": True,
            "data": result
        }, 201
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }, 400
    except Exception as e:
        raise e

@jwt_required()
@stats_bp.route("/<int:stats_id>", methods=["PUT"])
def update_stats(stats_id):
    try:
        data = request.get_json() or {}
        result = update_stats(stats_id, data)
        return {
            "success": True,
            "data": result
        }, 200
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }, 400
    except Exception as e:
        raise e
