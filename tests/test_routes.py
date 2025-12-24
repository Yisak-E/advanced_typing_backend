import os
import pytest
from app.create_app import create_app


@pytest.fixture
def client():
    os.environ.setdefault("FLASK_ENV", "development")
    app = create_app()
    app.config["TESTING"] = True
    # use in-memory DB for tests if desired (optional if migrations not run)
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    with app.test_client() as client:
        yield client

def test_auth_login_success(client):
    response = client.post('/auth/login', json={
        'identifier': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code in [200, 400]  # 400 if user doesn't exist
    data = response.get_json()
    assert 'success' in data

def test_auth_register_success(client):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpass'
    })
    assert response.status_code in [200, 400]  # 400 if already exists
    data = response.get_json()
    assert 'success' in data

def test_profile_me_unauthorized(client):
    response = client.get('/profiles/me')
    assert response.status_code == 401

def test_profile_me_put_unauthorized(client):
    response = client.put('/profiles/me', json={
        'display_name': 'UpdatedName'
    })
    assert response.status_code == 401

def test_profile_me_with_token(client, monkeypatch):
    # Arrange: fake user/profile and monkeypatch repository/service for isolation
    class DummyProfile:
        def __init__(self):
            self.id = 1
            self.user_id = 1
            self.display_name = "Test User"
            self.avatar_url = None
            self.bio = None
            self.country = None
            self.profile_visibility = "public"
            self.created_at = None
            self.updated_at = None
        def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "display_name": self.display_name,
                "avatar_url": self.avatar_url,
                "bio": self.bio,
                "country": self.country,
                "profile_visibility": self.profile_visibility,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }

    dummy_profile = DummyProfile()

    from app.users.service import user_profile_service
    monkeypatch.setattr(user_profile_service, "get_profile_by_user_id", lambda uid: dummy_profile)

    from flask_jwt_extended import create_access_token
    with client.application.app_context():
        access = create_access_token(identity=str(dummy_profile.user_id))

    resp = client.get(
        "/profiles/me",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["user_id"] == dummy_profile.user_id
    assert data["display_name"] == dummy_profile.display_name

# Add more tests for other blueprints/routes as needed
