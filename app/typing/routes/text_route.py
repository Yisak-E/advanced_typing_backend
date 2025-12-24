from flask import Blueprint, request

from app.typing.service.typing_text_service import get_typing_text_by_id, get_all_typing_texts, create_typing_text, \
    update_typing_text, delete_typing_text

text_bp = Blueprint('text_bp', __name__, url_prefix='/texts')

@text_bp.route('/<int:text_id>', methods=['GET'])
def get_text_by_id(text_id):
    try:
        result = get_typing_text_by_id(text_id)

        return {
            "success": True,
            "data": result
        }, 200

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }, 404

    except Exception as e:
        raise e

@text_bp.route('/', methods=['GET'])
def get_all_texts():
    try:
        result = get_all_typing_texts()

        return {
            "success": True,
            "data": result
        }, 200

    except Exception as e:
        raise e


# Additional routes for creating, updating, and deleting typing texts can be added here.
@text_bp.route('/', methods=['POST'])
def create_text():
    try:
        data = request.get_json() or {}
        result = create_typing_text(data)

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

@text_bp.route('/<int:text_id>', methods=['PUT'])
def update_text(text_id):
    try:
        data = request.get_json() or {}
        result = update_typing_text(text_id, data)

        return {
            "success": True,
            "data": result
        }, 200

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }, 404

    except Exception as e:
        raise e

@text_bp.route('/<int:text_id>', methods=['DELETE'])
def delete_text(text_id):
    try:
        delete_typing_text(text_id)

        return {
            "success": True,
            "message": "Typing text deleted successfully"
        }, 200

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }, 404

    except Exception as e:
        raise e



