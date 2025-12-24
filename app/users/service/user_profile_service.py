from app.extensions import db
from app.users.repository import user_profile_repository


def get_profile_by_user_id(user_id):
    return user_profile_repository.find_by_user_id(user_id)


def update_profile(user_id, data):
    profile = user_profile_repository.find_by_user_id(user_id)

    if not profile:
        raise ValueError("Profile not found")

    for field in [
        "display_name",
        "bio",
        "avatar_url",
        "country",
        "profile_visibility",
    ]:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()
    return profile
