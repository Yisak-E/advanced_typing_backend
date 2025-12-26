from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.auth.service.auth_service import login_user, register_user, logout_user, refresh_access_token

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
        }), 201

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        raise e


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    try:
        jti = get_jwt().get("jti")
        logout_user(jti)
        return jsonify({"success": True}), 200
    except Exception as e:
        raise e


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        jti = get_jwt().get("jti")
        user_id = get_jwt_identity()
        result = refresh_access_token(jti=jti, user_id=user_id)
        return jsonify({"success": True, "data": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        raise e
