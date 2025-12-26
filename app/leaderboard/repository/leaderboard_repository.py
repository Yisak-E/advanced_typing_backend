from datetime import date

from app.extensions import db
from app.leaderboard.models.leaderboard import Leaderboard


class LeaderRepository:
    def get_leaderboard(self, limit=None, recorded_at: date | None = None):
        query = Leaderboard.query
        if recorded_at:
            query = query.filter_by(recorded_at=recorded_at)
        query = query.order_by(Leaderboard.wpm.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def upsert_leaderboard(self, user_id, wpm):
        today = date.today()
        entry = Leaderboard.query.filter_by(user_id=user_id, recorded_at=today).first()
        if entry:
            entry.wpm = max(entry.wpm, wpm)
        else:
            entry = Leaderboard(user_id=user_id, wpm=wpm, rank=0, recorded_at=today)
            db.session.add(entry)
        db.session.commit()
        self.recalculate_ranks(recorded_at=today)
        db.session.commit()
        return entry

    def reset_leaderboard(self):
        Leaderboard.query.delete()

    def get_user_rank(self, user_id):
        entry = Leaderboard.query.filter_by(user_id=user_id).order_by(Leaderboard.recorded_at.desc()).first()
        return entry.rank if entry else None

    def save_leaderboard_entry(self, entry):
        db.session.add(entry)
        return entry

    def recalculate_ranks(self, recorded_at: date | None = None):
        query = Leaderboard.query
        if recorded_at:
            query = query.filter_by(recorded_at=recorded_at)
        entries = query.order_by(Leaderboard.wpm.desc()).all()
        for idx, entry in enumerate(entries, start=1):
            entry.rank = idx
        return entries
