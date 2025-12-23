import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "fallback-jwt-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://typing_user:1234@localhost/typing_club_adv"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config_mapping = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
