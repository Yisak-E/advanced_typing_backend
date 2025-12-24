"""
| Column Name    | Data Type | Constraints / Notes |
| -------------- | --------- | ------------------- |
| id             | INT       | PK                  |
| user_id        | INT       | FK → users.id       |
| wpm            | INT       | NOT NULL            |
| accuracy       | FLOAT     | NOT NULL            |
| chars_typed    | INT       | NOT NULL            |
| time_spent_sec | INT       | NOT NULL            |
| created_at     | DATETIME  | default = now       |

"""

from app.extensions import db

class TypingStats(db.Model):
    __tablename__ = "typing_stats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    wpm = db.Column(db.Integer, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    chars_typed = db.Column(db.Integer, nullable=False)
    time_spent_sec = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<TypingStats id={self.id} user_id={self.user_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wpm": self.wpm,
            "accuracy": self.accuracy,
            "chars_typed": self.chars_typed,
            "time_spent_sec": self.time_spent_sec,
            "created_at": self.created_at.isoformat()
        }