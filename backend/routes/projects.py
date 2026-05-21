from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db
from ..models.project import Project
from ..models.user import User

projects_bp = Blueprint('projects', __name__)

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if current_user['role'] == 'admin':
        projects = Project.query.all()
    else:
        projects = user.projects

    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_project():
    try:
        current_user = get_jwt_identity()
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({'error': 'Invalid or missing JSON'}), 400

        from datetime import datetime
        deadline = None
        if data.get('deadline'):
            deadline = datetime.fromisoformat(data['deadline'])

        project = Project(
            name=data['name'],
            description=data.get('description', ''),
            deadline=deadline,
            owner_id=current_user['id']
        )

        db.session.add(project)
        db.session.commit()

        return jsonify(project.to_dict()), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"Server error: {str(e)}"}), 500


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()

        from datetime import datetime
        if data.get('name'):
            project.name = data['name']
        if data.get('description'):
            project.description = data['description']
        if data.get('deadline'):
            project.deadline = datetime.fromisoformat(data['deadline'])

        db.session.commit()
        return jsonify(project.to_dict()), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"Server error: {str(e)}"}), 500


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200


@projects_bp.route('/<int:project_id>/members', methods=['POST'])
@jwt_required()
@admin_required
def add_member(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()

    user = User.query.get(data.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user in project.members:
        return jsonify({'error': 'User already a member'}), 409

    project.members.append(user)
    db.session.commit()
    return jsonify(project.to_dict()), 200


@projects_bp.route('/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def remove_member(project_id, user_id):
    project = Project.query.get_or_404(project_id)
    user = User.query.get_or_404(user_id)

    if user not in project.members:
        return jsonify({'error': 'User not a member'}), 404

    project.members.remove(user)
    db.session.commit()
    return jsonify(project.to_dict()), 200