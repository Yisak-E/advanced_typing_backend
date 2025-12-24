from app.extensions import db
from app.stats.models.typing_stats import TypingStats


class StatsRepository:
    def get_stats(self):
        return TypingStats.query.all()

    def get_stats_by_id(self, stats_id):
        return TypingStats.query.filter_by(id=stats_id).first()

    def get_stats_by_user_id(self, user_id):
        return TypingStats.query.filter_by(user_id=user_id).all()

    def save_stats(self, stats):
        db.session.add(stats)
        return stats

    def delete_stats(self, stats_id):
        stats = self.get_stats_by_id(stats_id)
        db.session.delete(stats)

    def update_stats(self, stats_id, stats_data):
        stats = self.get_stats_by_id(stats_id)
        for key, value in stats_data.items():
            setattr(stats, key, value)
        db.session.add(stats)
        return stats