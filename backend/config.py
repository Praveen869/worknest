import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'worknest-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'worknest-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_VERIFY_SUB = False

    @staticmethod
    def init_app(app):
        db_url = os.environ.get('DATABASE_URL', '')
        if db_url.startswith('postgres://'):
            os.environ['DATABASE_URL'] = db_url.replace('postgres://', 'postgresql://', 1)
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']