import os
from flask import Flask
from app.extensions import db, migrate, jwt, cors
from app.config import config_mapping
from app.auth.routes.auth_route import auth_bp
from app.leaderboard.routes import leader_bp
from app.stats.routes import stats_bp
from app.typing.routes import text_bp
from app.users.routes.profile_route import profile_bp

def create_app():
    app = Flask(__name__)

    # 👇 FIX: define config_class properly
    env = os.environ.get("FLASK_ENV", "development")
    config_class = config_mapping.get(env)

    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def handle_missing_token(err):
        return {"error": err}, 401

    @jwt.invalid_token_loader
    def handle_invalid_token(err):
        return {"error": err}, 401

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return {"error": "Token has expired"}, 401

    cors.init_app(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
        supports_credentials=True,
    )

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(text_bp)
    app.register_blueprint(leader_bp)

    return app
