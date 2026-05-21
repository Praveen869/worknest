from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import os
import json

# --- PyJWT 2.10.0+ Compatibility Patch ---
import flask_jwt_extended

original_get_jwt_identity = flask_jwt_extended.get_jwt_identity

def patched_get_jwt_identity():
    identity = original_get_jwt_identity()
    if isinstance(identity, str):
        try:
            return json.loads(identity)
        except Exception:
            pass
    return identity

flask_jwt_extended.get_jwt_identity = patched_get_jwt_identity
# -----------------------------------------

from .config import Config
from .models import db
from .models.user import User
from .models.project import Project
from .models.task import Task

from .routes.auth import auth_bp
from .routes.projects import projects_bp
from .routes.tasks import tasks_bp
from .routes.dashboard import dashboard_bp

app = Flask(__name__,
    static_folder='../frontend/static',
    template_folder='../frontend/templates'
)

app.config.from_object(Config)
Config.init_app(app)

# Extensions
# Ensure DATABASE_URL is configured before initializing the DB extension
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    raise RuntimeError('DATABASE_URL is not set. Configure your DATABASE_URL environment variable (e.g. from Railway Postgres plugin)')

db.init_app(app)
jwt = JWTManager(app)

from flask import jsonify

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({'error': f'Invalid token: {error_string}'}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    return jsonify({'error': error_string}), 401

@jwt.user_identity_loader
def user_identity_lookup(identity_data):
    if isinstance(identity_data, dict):
        return json.dumps(identity_data)
    return str(identity_data)

CORS(app)  # type: ignore
migrate = Migrate(app, db)  # type: ignore

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(projects_bp, url_prefix='/projects')
app.register_blueprint(tasks_bp, url_prefix='/tasks')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

# Serve Frontend
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/projects')
def projects_page():
    return render_template('projects.html')

@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)