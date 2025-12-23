import os
from flask import Flask
from app.extensions import db, migrate, jwt, cors
from app.config import config_mapping
from app.auth.routes.auth_route import auth_bp

def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "development")
    config_class = config_mapping.get(env, config_mapping["development"])
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:3000"]
            }
        }
    )

    app.register_blueprint(auth_bp)

    return app
