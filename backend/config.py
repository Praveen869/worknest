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
            # Strip any query parameters like ?sslmode=require for pg8000
            # because pg8000 uses standard Python ssl_context instead of sslmode kwarg
            if 'pg8000' in db_url:
                import re
                db_url = re.sub(r'[&?]sslmode=[^&]*', '', db_url)
                
                # Configure SSL Context only for remote databases (not localhost/127.0.0.1)
                # to prevent local development database connection from failing.
                if 'localhost' not in db_url and '127.0.0.1' not in db_url:
                    import ssl
                    ssl_context = ssl.create_default_context()
                    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                        "connect_args": {
                            "ssl_context": ssl_context
                        }
                    }

            os.environ['DATABASE_URL'] = db_url
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url