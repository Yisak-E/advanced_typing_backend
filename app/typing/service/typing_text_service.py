from app.extensions import db
from app.typing.models.typing import TypingText
from app.typing.repository.text_repository import TypingTextRepository

text_repo = TypingTextRepository()

def create_typing_text(input_data):
    level = input_data.get("level")
    content = input_data.get("content")
    language = input_data.get("language", "en")

    if not level or not content:
        raise ValueError("Level and content are required")

    typing_text = TypingText(
        level=level,
        content=content,
        language=language
    )

    text_repo.save(typing_text)
    db.session.commit()

    return {
        "typing_text": typing_text.serialize()
    }

def get_typing_text_by_id(text_id):
    typing_text = text_repo.find_by_id(text_id)
    if not typing_text:
        raise ValueError("Typing text not found")

    return {
        "typing_text": typing_text.serialize()
    }

def get_all_typing_texts():
    texts = text_repo.get_all_texts()
    return {
        "typing_texts": [text.serialize() for text in texts]
    }

def update_typing_text(text_id, input_data):
    typing_text = text_repo.find_by_id(text_id)
    if not typing_text:
        raise ValueError("Typing text not found")

    level = input_data.get("level")
    content = input_data.get("content")
    language = input_data.get("language")

    if level:
        typing_text.level = level
    if content:
        typing_text.content = content
    if language:
        typing_text.language = language

    text_repo.save(typing_text)
    db.session.commit()

    return {
        "typing_text": typing_text.serialize()
    }

def delete_typing_text(text_id):
    typing_text = text_repo.find_by_id(text_id)
    if not typing_text:
        raise ValueError("Typing text not found")

    text_repo.delete(typing_text)
    db.session.commit()

    return {
        "message": "Typing text deleted successfully"
    }

def get_typing_texts_by_level(level):
    texts = text_repo.find_by_level(level)
    return {
        "typing_texts": [text.serialize() for text in texts]
    }

def get_typing_texts_by_language(language):
    texts = text_repo.find_by_language(language)
    return {
        "typing_texts": [text.serialize() for text in texts]
    }