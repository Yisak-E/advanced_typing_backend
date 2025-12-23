from app.auth.models.user import User
from app.extensions import db


class UserRepository:

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def find_by_id(self, user_id):
        return User.query.get(user_id)

    def save(self, user):
        db.session.add(user)
        return user

    def delete(self, user):
        db.session.delete(user)
