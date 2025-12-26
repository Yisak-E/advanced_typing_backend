from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class TypingText(db.Model):
    __tablename__ = "typing_texts"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Enum("beginner", "intermediate", "advanced"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False, default="en")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )
    def __repr__(self):
        return f"<Typing id={self.id}>"
    def serialize(self):
        return {
            "id": self.id,
            "level": self.level,
            "content": self.content,
            "language": self.language,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }