from datetime import datetime, timedelta, date
from app.create_app import create_app
from app.extensions import db

from app.auth.models.user import User
from app.users.models.user_profile import UserProfile
from app.auth.models.refresh_token import RefreshToken
from app.typing.models.typing import TypingText
from app.stats.models.typing_stats import TypingStats as TypingStat
from app.leaderboard.models.leaderboard import Leaderboard


def reset_tables():
    """
    Delete in correct order (children -> parents) to avoid FK errors.
    """
    db.session.query(Leaderboard).delete()
    db.session.query(TypingStat).delete()
    db.session.query(RefreshToken).delete()
    db.session.query(UserProfile).delete()
    db.session.query(TypingText).delete()
    db.session.query(User).delete()
    db.session.commit()


def seed():
    print("🌱 Resetting tables...")
    reset_tables()

    print("👤 Creating users...")
    users = []
    for i in range(1, 8):
        u = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            role="user",
            is_active=True,
        )
        u.set_password("password123")  # uses your model method
        users.append(u)

    db.session.add_all(users)
    db.session.commit()

    print("🧾 Creating user profiles...")
    profiles = []
    for u in users:
        profiles.append(
            UserProfile(
                user_id=u.id,
                display_name=u.username.capitalize(),
                bio=f"Hello! I'm {u.username} and I love typing.",
                avatar_url="",
                country="UAE",
                profile_visibility="public",
            )
        )
    db.session.add_all(profiles)
    db.session.commit()

    print("📝 Creating typing texts (level enum)...")
    texts = [
        # beginner (at least 7 overall, but include all levels)
        ("beginner", "The quick brown fox jumps over the lazy dog.", "en"),
        ("beginner", "Typing is a useful skill for every programmer.", "en"),
        ("beginner", "Practice daily to improve speed and accuracy.", "en"),

        # intermediate
        ("intermediate", "Flask uses Blueprints to organize routes and modules.", "en"),
        ("intermediate", "JWT tokens are commonly used for stateless authentication.", "en"),

        # advanced
        ("advanced", "Asynchronous I/O improves throughput when handling many network requests.", "en"),
        ("advanced", "Database normalization reduces redundancy but can increase join complexity.", "en"),
    ]

    typing_texts = []
    for lvl, content, lang in texts:
        typing_texts.append(TypingText(level=lvl, content=content, language=lang))

    db.session.add_all(typing_texts)
    db.session.commit()

    print("📊 Creating typing stats...")
    # NOTE: adjust field names here if your TypingStat model differs
    stats = []
    for idx, u in enumerate(users, start=1):
        stats.append(
            TypingStat(
                user_id=u.id,
                wpm=45 + idx * 5,
                accuracy=88 + idx,
                duration_seconds=60,
                created_at=datetime.utcnow() - timedelta(days=idx),
            )
        )
    db.session.add_all(stats)
    db.session.commit()

    print("🔐 Creating refresh tokens...")
    refresh_tokens = []
    for u in users:
        refresh_tokens.append(
            RefreshToken(
                token=f"seed-refresh-token-{u.id}-{int(datetime.utcnow().timestamp())}",
                user_id=u.id,
                expires_at=datetime.utcnow() + timedelta(days=7),
                revoked=False,
            )
        )
    db.session.add_all(refresh_tokens)
    db.session.commit()

    print("🏆 Creating leaderboard entries...")
    # Rank 1 is best (highest wpm)
    leaderboard_rows = []
    sorted_users = sorted(users, key=lambda x: x.id)  # stable
    for rank, u in enumerate(sorted_users, start=1):
        leaderboard_rows.append(
            Leaderboard(
                user_id=u.id,
                wpm=120 - rank * 4,
                rank=rank,
                recorded_at=date.today(),
            )
        )
    db.session.add_all(leaderboard_rows)
    db.session.commit()

    print("✅ Seed complete! (7+ rows each table)")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
