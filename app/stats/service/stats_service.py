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


def get_stats_summary_by_user_id(user_id):
    stats = stats_repo.get_stats_by_user_id(user_id)
    if not stats:
        return {"wpm_avg": 0, "accuracy_avg": 0, "sessions": 0}
    wpm_avg = sum(s.wpm or 0 for s in stats) / len(stats)
    acc_avg = sum(s.accuracy or 0 for s in stats) / len(stats)
    return {"wpm_avg": wpm_avg, "accuracy_avg": acc_avg, "sessions": len(stats)}


def create_stats(input_data):
    user_id = input_data.get("user_id")
    wpm = input_data.get("wpm")
    accuracy = input_data.get("accuracy")
    duration_seconds = input_data.get("duration_seconds")
    chars_typed = input_data.get("chars_typed")

    if not user_id or wpm is None or accuracy is None or duration_seconds is None or chars_typed is None:
        raise ValueError("All fields are required")

    stats = TypingStats(
        user_id=user_id,
        wpm=wpm,
        accuracy=accuracy,
        duration_seconds=duration_seconds,
        chars_typed=chars_typed,
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

    for field in ["wpm", "accuracy", "duration_seconds", "chars_typed"]:
        if field in input_data:
            setattr(stats, field, input_data[field])

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
