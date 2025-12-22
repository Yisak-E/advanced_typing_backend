from flask import jsonify

from app.auth.models.user import User
from app.core import db


class UserRepository:
    
    def find_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        
        return user if user else None

    def find_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user if user else None
    

    def create_user(self, username, email, password, role='user'):
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()
        return True