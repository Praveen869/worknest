import sys
sys.path.append('backend')

# Patch before importing app
import flask_jwt_extended
import json

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

from app import app, jwt
from models import db
from models.user import User
from flask_jwt_extended import create_access_token

# Define user identity loader
@jwt.user_identity_loader
def user_identity_lookup(identity_data):
    if isinstance(identity_data, dict):
        return json.dumps(identity_data)
    return str(identity_data)

with app.app_context():
    # Find or create a test admin user
    user = User.query.filter_by(role='admin').first()
    if not user:
        user = User(name='Test Admin', email='admin@test.com', role='admin')
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
    
    # Generate token
    token = create_access_token(identity={'id': user.id, 'role': user.role})
    print(f"Generated Token: {token}")

    # Simulate client request
    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test dashboard endpoint
        response = client.get('/dashboard/', headers=headers)
        print(f"Dashboard Response Code: {response.status_code}")
        print(f"Dashboard Response JSON: {response.get_json()}")
        
        # Test project creation endpoint
        response_proj = client.post('/projects/', json={'name': 'Test Project'}, headers=headers)
        print(f"Create Project Response Code: {response_proj.status_code}")
        print(f"Create Project Response JSON: {response_proj.get_json()}")
