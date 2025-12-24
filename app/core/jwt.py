from datetime import timedelta
from flask_jwt_extended import create_access_token as _create_access_token
from flask_jwt_extended import create_refresh_token as _create_refresh_token


def _user_id(user):
    return user.id if hasattr(user, "id") else user


def create_access_token(user):
    """
    Create a short-lived access token.
    """
    user_obj = user if hasattr(user, "id") else None
    user_id = _user_id(user)
    claims = {}
    if user_obj:
        claims = {
            "role": user_obj.role,
            "email": user_obj.email,
        }
    return _create_access_token(
        identity=str(user_id),
        additional_claims=claims,
        expires_delta=timedelta(minutes=15),
    )


def create_refresh_token(user):
    """
    Create a long-lived refresh token.
    """
    return _create_refresh_token(
        identity=str(_user_id(user)),
        expires_delta=timedelta(days=7),
    )
