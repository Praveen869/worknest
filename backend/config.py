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
        # Normalize older Heroku-style URL and prefer a pure-Python driver (pg8000)
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)

        # If the URL uses plain postgresql://, rewrite to postgresql+pg8000://
        # so SQLAlchemy picks the pure-Python `pg8000` driver (avoids libpq).
        if db_url.startswith('postgresql://') and 'pg8000' not in db_url:
            db_url = db_url.replace('postgresql://', 'postgresql+pg8000://', 1)

        if db_url:
            os.environ['DATABASE_URL'] = db_url
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url