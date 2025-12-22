# AuthService IS RESPONSIBLE FOR:
#     - validating input
#     - applying business rules
#     - coordinating models & repositories

# AuthService IS NOT RESPONSIBLE FOR:
#     - HTTP requests / responses
#     - direct database access
#     - JWT configuration details


from app.auth.models.user import User
from app.core import db
from app.users.models.user_profile import UserProfile


def register_user(input_data):

    username = input_data.get('username')
    email = input_data.get('email')
    password = input_data.get('password')
    role = input_data.get('role', 'user')
    # Input validation
    if None in [username, email, password]:
        raise ValueError("Username, email, and password are required.")
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long.")
    # Business rules
    existing_user = User.find_by_email(email)
    if existing_user:
        raise ValueError("Email already registered.")
    # Create user
    user = User.create_user(username, email, password, role)

    # save user using user-repository (if exists)

    userProfile = UserProfile(
        user_id=user.id, 
        display_name=username,
        profile_visibility='public'
    )
    # save user profile using user-profile-repository (if exists)



def login_user(input_data):
    email_or_username = input_data.get('username', 'email')
    password = input_data.get('password')
    # Input validation
    if None in [email_or_username, password]:
        raise ValueError("Email and password are required.")
    # Find user
    user = User.find_by_email(email_or_username)
    if not user:
        user = User.find_by_username(email_or_username)

    if not user or not user.check_password(password):
        raise ValueError("Invalid email or password.")
    if not user.is_active:
        raise ValueError("User account is deactivated.")
    # Update last login
    user.update_last_login()
    access_token = user.generate_jwt()
    refrash_token = user.generate_refresh_jwt()

    return {
        'access_token': access_token,
        'refresh_token': refrash_token,
        'user': user.to_dict()
    }


# FUNCTION logout_user(user_id, refresh_token):

    # FIND RefreshToken BY token
    #     IF not found:
    #         RETURN success (idempotent)

    # MARK RefreshToken AS revoked

    # SAVE RefreshToken

    # RETURN success


def logout_user(user_id, refresh_token):

    token = RefreshToken.find_by_token(refresh_token)
    if not token:
        return  # Idempotent logout

    token.revoked = True
    db.session.commit()

# FUNCTION logout_user(user_id, refresh_token):

#     FIND RefreshToken BY token
#         IF not found:
#             RETURN success (idempotent)

#     MARK RefreshToken AS revoked

#     SAVE RefreshToken

#     RETURN success

def refresh_access_token(refresh_token):
    token = RefreshToken.find_by_token(refresh_token)
    if not token or token.revoked:
        raise ValueError("Invalid refresh token.")
    user = User.find_by_id(token.user_id)
    if not user or not user.is_active:
        raise ValueError("User account is deactivated.")
    new_access_token = user.generate_jwt()
    return {
        'access_token': new_access_token
    }

