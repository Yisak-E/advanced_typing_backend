from datetime import timedelta
from flask_jwt_extended import create_access_token as _create_access_token
from flask_jwt_extended import create_refresh_token as _create_refresh_token


def create_access_token(user):
    """
    Create a short-lived access token.
    """
    return _create_access_token(
        identity=user.id,
        additional_claims={
            "role": user.role,
            "email": user.email,
        },
        expires_delta=timedelta(minutes=15),
    )


def create_refresh_token(user):
    """
    Create a long-lived refresh token.
    """
    return _create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=7),
    )
