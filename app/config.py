import os




class BaseConfig:

    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')

class DevelopmentConfig(BaseConfig):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_database.db'

class ProductionConfig(BaseConfig):
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod_database.db')

config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
