"""
| Column Name | Data Type | Constraints / Notes |
| ----------- | --------- | ------------------- |
| id          | INT       | PK                  |
| user_id     | INT       | FK → users.id       |
| wpm         | INT       | NOT NULL            |
| rank        | INT       | NOT NULL            |
| recorded_at | DATE      | indexed             |

"""
from app.extensions import db
class Leaderboard(db.Model):

    __tablename__ = "leaderboard"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    wpm = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    recorded_at = db.Column(db.Date, index=True, nullable=False)

    def __repr__(self):
        return f"<Leaderboard id={self.id} user_id={self.user_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wpm": self.wpm,
            "rank": self.rank,
            "recorded_at": self.recorded_at.isoformat()
        }
