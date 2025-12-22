

from app.auth.models.refresh_token import RefreshToken
from app.core import db


class RefreshTokenRepository:
    def find_by_token(self, token):
        refresh_token = RefreshToken.query.filter_by(token=token).first()
        return refresh_token
    
    def save(self, refresh_token):
        db.session.add(refresh_token)
        db.session.commit()
        return refresh_token
    
    def revoke(self, refresh_token):
        db.session.delete(refresh_token)
        db.session.commit()
        return True