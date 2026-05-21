import sys
sys.path.append('backend')
from app import app
from models import db
from models.user import User
from flask_jwt_extended import create_access_token

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
