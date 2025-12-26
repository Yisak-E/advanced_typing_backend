from app.users.models.user_profile import UserProfile
from app.extensions import db

class UserProfileRepository:
    def find_by_user_id(self, user_id: int):
        return UserProfile.query.filter_by(user_id=user_id).first()

    def find_all(self):
        profile_list = UserProfile.query.all()
        serialized_profile_list = []
        for profile in profile_list:
            serialized_profile_list.append(profile.serialize())
        return serialized_profile_list


    def save(self, user_profile, flush=False):
        db.session.add(user_profile)
        if flush:
            db.session.flush()
        return user_profile

    def delete(self, user_profile):
        db.session.delete(user_profile)

user_profile_repository = UserProfileRepository()
