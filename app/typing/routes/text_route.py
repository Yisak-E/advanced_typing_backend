from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.typing.service.typing_text_service import (
    get_typing_text_by_id,
    get_all_typing_texts,
    create_typing_text,
    update_typing_text,
    delete_typing_text,
    get_typing_texts_by_level,
)

text_bp = Blueprint('typing', __name__, url_prefix='/typing')


@text_bp.get('/texts')
def get_texts():
    level = request.args.get('level')
    if level:
        result = get_typing_texts_by_level(level)
    else:
        result = get_all_typing_texts()
    return jsonify({"success": True, "data": result}), 200


@text_bp.route('/texts/<int:text_id>', methods=['GET'])
def get_text_by_id_route(text_id):
    try:
        result = get_typing_text_by_id(text_id)
        return jsonify({"success": True, "data": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@text_bp.post('/texts')
@jwt_required()
def create_text():
    # TODO: enforce admin role check via claims if roles are used
    try:
        data = request.get_json() or {}
        result = create_typing_text(data)
        return jsonify({"success": True, "data": result}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@text_bp.route('/texts/<int:text_id>', methods=['PUT'])
@jwt_required()
def update_text(text_id):
    # TODO: enforce admin role check via claims if roles are used
    try:
        data = request.get_json() or {}
        result = update_typing_text(text_id, data)
        return jsonify({"success": True, "data": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@text_bp.route('/texts/<int:text_id>', methods=['DELETE'])
@jwt_required()
def delete_text_route(text_id):
    # TODO: enforce admin role check via claims if roles are used
    try:
        delete_typing_text(text_id)
        return jsonify({"success": True, "message": "Typing text deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
