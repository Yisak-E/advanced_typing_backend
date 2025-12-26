from datetime import date

from app.extensions import db
from app.leaderboard.models.leaderboard import Leaderboard
from app.leaderboard.repository.leaderboard_repository import LeaderRepository

repo = LeaderRepository()


def get_leaderboard(limit=None):
    leaderboard = repo.get_leaderboard(limit=limit)
    return {"leaderboard": [entry.serialize() for entry in leaderboard]}


def get_daily_leaderboard():
    today = date.today()
    leaderboard = repo.get_leaderboard(limit=None, recorded_at=today)
    return {"leaderboard": [entry.serialize() for entry in leaderboard]}


def update_leaderboard(user_id, wpm):
    updated_entry = repo.upsert_leaderboard(user_id, wpm)
    return {"leaderboard_entry": updated_entry.serialize()}


def reset_leaderboard():
    repo.reset_leaderboard()
    db.session.commit()
    return {"message": "Leaderboard has been reset"}


def get_user_rank(user_id):
    rank = repo.get_user_rank(user_id)
    return {"user_id": user_id, "rank": rank}


def save_leaderboard_entry(input_data):
    user_id = input_data.get("user_id")
    wpm = input_data.get("wpm")
    if not user_id or wpm is None:
        raise ValueError("User ID and wpm are required")

    today = date.today()
    entry = Leaderboard(user_id=user_id, wpm=wpm, rank=0, recorded_at=today)
    saved_entry = repo.save_leaderboard_entry(entry)
    db.session.commit()
    repo.recalculate_ranks(recorded_at=today)
    db.session.commit()
    return {"leaderboard_entry": saved_entry.serialize()}
