from app.extensions import db
from app.stats.models.typing_stats import TypingStats
from app.stats.repository.stats_repository import StatsRepository

stats_repo = StatsRepository()

def get_all_stats():
    stats = stats_repo.get_stats()
    return {
        "stats": [stat.serialize() for stat in stats]
    }

def get_stats_by_user_id(user_id):
    stats = stats_repo.get_stats_by_user_id(user_id)
    return {
        "stats": [stat.serialize() for stat in stats]
    }

def create_stats(input_data):
    user_id = input_data.get("user_id")
    wpm = input_data.get("wpm")
    accuracy = input_data.get("accuracy")
    duration = input_data.get("duration")

    if not user_id or wpm is None or accuracy is None or duration is None:
        raise ValueError("All fields are required")

    stats = TypingStats(
        user_id=user_id,
        wpm=wpm,
        accuracy=accuracy,
        duration=duration
    )

    stats_repo.save_stats(stats)
    db.session.commit()

    return {
        "stats": stats.serialize()
    }

def update_stats(stats_id, input_data):
    stats = stats_repo.get_stats_by_id(stats_id)
    if not stats:
        raise ValueError("Stats not found")

    wpm = input_data.get("wpm")
    accuracy = input_data.get("accuracy")
    duration = input_data.get("duration")

    if wpm is not None:
        stats.wpm = wpm
    if accuracy is not None:
        stats.accuracy = accuracy
    if duration is not None:
        stats.duration = duration

    stats_repo.save_stats(stats)
    db.session.commit()

    return {
        "stats": stats.serialize()
    }

def delete_stats(stats_id):
    stats = stats_repo.get_stats_by_id(stats_id)
    if not stats:
        raise ValueError("Stats not found")

    stats_repo.delete_stats(stats_id)
    db.session.commit()

    return {
        "message": "Stats deleted successfully"
    }

