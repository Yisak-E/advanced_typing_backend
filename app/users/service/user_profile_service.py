from app.users.models.user_profile import UserProfile
from app.extensions import db


ALLOWED_PROFILE_FIELDS = {
    "display_name",
    "bio",
    "avatar_url",
    "country",
    "profile_visibility",
}


def update_profile(user_id, data, user_profile_repository):

    profile = user_profile_repository.find_by_user_id(user_id)

    if not profile:
        profile = UserProfile(user_id=user_id)
        user_profile_repository.save(profile)

    for key, value in data.items():
        if key in ALLOWED_PROFILE_FIELDS:
            setattr(profile, key, value)

    db.session.commit()

    return profile
