
from app.users.models.user_profile import UserProfile


class UserProfileRepository:

    def get_user_profile_by_id(self,user_id):
        return UserProfile.query.filter_by(user_id=user_id).first()
    
    def save_user_profile(self, user_profile):
        from app.extensions import db
        db.session.add(user_profile)
        db.session.commit()
        return user_profile