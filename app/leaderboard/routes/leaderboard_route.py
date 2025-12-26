from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.leaderboard.service import leader_service

leader_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leader_bp.route("", methods=["GET"])
def get_leaderboard():
    result = leader_service.get_leaderboard()
    return jsonify({"success": True, "data": result}), 200


@leader_bp.route("/daily", methods=["GET"])
def get_daily():
    result = leader_service.get_daily_leaderboard()
    return jsonify({"success": True, "data": result}), 200


@leader_bp.route("/", methods=["POST"])
@jwt_required()
def save_leaderboard_entry():
    data = request.get_json() or {}
    try:
        result = leader_service.save_leaderboard_entry(data)
        return jsonify({"success": True, "data": result}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@leader_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_leaderboard():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    wpm = data.get("wpm")

    if not user_id or wpm is None:
        return jsonify({"success": False, "error": "User ID and wpm are required"}), 400

    result = leader_service.update_leaderboard(user_id, wpm)
    return jsonify({"success": True, "data": result}), 200


@leader_bp.route("/reset", methods=["POST"])
@jwt_required()
def reset_leaderboard():
    result = leader_service.reset_leaderboard()
    return jsonify({"success": True, "data": result}), 200


@leader_bp.route("/rank/<int:user_id>", methods=["GET"])
def get_user_rank(user_id):
    result = leader_service.get_user_rank(user_id)
    return jsonify({"success": True, "data": result}), 200
