from app.auth.models.refresh_token import RefreshToken
from app.extensions import db


class RefreshTokenRepository:
    def save(self, refresh_token, flush=False):
        db.session.add(refresh_token)
        if flush:
            db.session.flush()
        return refresh_token

    def find_by_token(self, token):
        return RefreshToken.query.filter_by(token=token).first()

    def revoke(self, refresh_token, commit=False):
        refresh_token.revoked = True
        if commit:
            db.session.commit()
        return refresh_token


refresh_token_repository = RefreshTokenRepository()
