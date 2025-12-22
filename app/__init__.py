import flask
from app.extensions import db, migrate, jwt, cors
from app.config import config_mapping



def create_app(config_name='development'):
    app = flask.Flask(__name__)
    config_class = config_mapping.get(config_name, config_mapping['development'])
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    """
            REGISTER blueprints:
                auth blueprint
                typing blueprint
                leaderboard blueprint
                chat blueprint

            DEFINE global error handlers:
                404 handler
                401 handler
                validation error handler
    """

    

    return app