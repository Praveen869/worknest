from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db
from models.task import Task
from models.project import Project
from models.user import User

tasks_bp = Blueprint('tasks', __name__)

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    project_id = request.args.get('project_id')

    if current_user['role'] == 'admin':
        if project_id:
            tasks = Task.query.filter_by(project_id=project_id).all()
        else:
            tasks = Task.query.all()
    else:
        user = User.query.get(current_user['id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        project_ids = [p.id for p in user.projects]

        if project_id:
            try:
                proj_id_int = int(project_id)
            except ValueError:
                return jsonify({'error': 'Invalid project id'}), 400

            if proj_id_int not in project_ids:
                return jsonify({'error': 'Access denied'}), 403
            tasks = Task.query.filter_by(project_id=proj_id_int).all()
        else:
            tasks = Task.query.filter(Task.project_id.in_(project_ids)).all() if project_ids else []

    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_task():
    data = request.get_json()

    if not data.get('title') or not data.get('project_id'):
        return jsonify({'error': 'Title and project_id required'}), 400

    project = Project.query.get(data['project_id'])
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    deadline = None
    if data.get('deadline'):
        deadline = datetime.fromisoformat(data['deadline'])

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        deadline=deadline,
        project_id=data['project_id'],
        assigned_to=data.get('assigned_to')
    )

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.get_or_404(task_id)

    # Member sirf apna task update kar sakta hai
    if current_user['role'] == 'member' and task.assigned_to != current_user['id']:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    if current_user['role'] == 'admin':
        if data.get('title'):
            task.title = data['title']
        if data.get('description'):
            task.description = data['description']
        if data.get('priority'):
            task.priority = data['priority']
        if data.get('assigned_to'):
            task.assigned_to = data['assigned_to']
        if data.get('deadline'):
            task.deadline = datetime.fromisoformat(data['deadline'])

    # Dono update kar sakte hain status
    if data.get('status'):
        if data['status'] not in ['todo', 'in_progress', 'done']:
            return jsonify({'error': 'Invalid status'}), 400
        task.status = data['status']

    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200