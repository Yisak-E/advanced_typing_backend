from flask import Blueprint, request, jsonify
from app.auth.service.auth_service import login_user, register_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}

        result = login_user(data)

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    
    except Exception as e:
        raise e

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}

        result = register_user(data)

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        raise e

