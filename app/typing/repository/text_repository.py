from app.typing.models.typing import TypingText
from app.extensions import db

class TypingTextRepository:
    def find_by_id(self, text_id):
        return TypingText.query.filter_by(id=text_id).first()

    def find_by_level(self, level):
        return TypingText.query.filter_by(level=level).all()

    def find_by_language(self, language):
        return TypingText.query.filter_by(language=language).all()

    def get_all_texts(self):
        return TypingText.query.all()

    def save(self, typing_text, flush=False):
        db.session.add(typing_text)
        if flush:
            db.session.flush()
        return typing_text

    def delete(self, typing_text):
        db.session.delete(typing_text)
        return True