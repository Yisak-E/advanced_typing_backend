import datetime


from app.auth.models.refresh_token import RefreshToken
from app.auth.models.user import User
from app.users.models.user_profile import UserProfile
from app.extensions import db
from app.auth.repository.user_repository import UserRepository
from app.users.repository.user_profile_repository import user_profile_repository
from app.auth.repository.refresh_token_repository import refresh_token_repository
from app.core.jwt import create_access_token, create_refresh_token


user_repository = UserRepository()


def register_user(input_data):
    username = input_data.get("username")
    email = input_data.get("email")
    password = input_data.get("password")
    role = input_data.get("role", "user")

    # ---------- validation ----------
    if not username or not email or not password:
        raise ValueError("Username, email, and password are required")

    if len(password) < 4:
        raise ValueError("Password too short")

    # ---------- business rules ----------
    if user_repository.find_by_email(email):
        raise ValueError("Email already registered")

    # ---------- create user ----------
    user = User(username=username, email=email, role=role)
    user.set_password(password)

    user_repository.save(user)
    db.session.flush()  # ensures user.id exists

    # ---------- create profile ----------
    profile = UserProfile(
        user_id=user.id,
        display_name=username,
        profile_visibility="public",
    )

    user_profile_repository.save(profile, False)

    db.session.commit()

    return {
        "user": user.serialize()
    }



def login_user(input_data):
    identifier = input_data.get("identifier")
    password = input_data.get("password")

    if not identifier or not password:
        raise ValueError("Identifier and password required")

    user = (
        user_repository.find_by_email(identifier)
        or user_repository.find_by_username(identifier)
    )

    if not user or not user.check_password(password):
        raise ValueError("Invalid credentials")

    if not user.is_active:
        raise ValueError("Account deactivated")

    access_token = create_access_token(user)
    refresh_token_str = create_refresh_token(user)

    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
    )

    refresh_token_repository.save(refresh_token, False)

    profile = (
        user_profile_repository.find_by_user_id(user.id)

    )
    db.session.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "user": user.serialize(),
        "profile": profile.serialize(),

    }




def logout_user(refresh_token_str):
    token = refresh_token_repository.find_by_token(refresh_token_str)

    if not token:
        return

    token.revoked = True
    db.session.commit()



def refresh_access_token(refresh_token_str):
    token = refresh_token_repository.find_by_token(refresh_token_str)

    if not token or not token.is_valid():
        raise ValueError("Invalid refresh token")

    user = user_repository.find_by_id(token.user_id)

    if not user or not user.is_active:
        raise ValueError("Account deactivated")

    return {
        "access_token": create_access_token(user)
    }
