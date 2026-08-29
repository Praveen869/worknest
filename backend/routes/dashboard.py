from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from ..models.task import Task
from ..models.project import Project
from ..models.user import User
from ..cache import get_cache, set_cache, get_last_cache_status

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_dashboard():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cache_key = f"dashboard:user:{current_user['id']}"
    cached_data = get_cache(cache_key)
    if cached_data:
        cached_data['cached'] = True
        return jsonify(cached_data), 200

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if current_user['role'] == 'admin':
        total_tasks = Task.query.count()
        todo = Task.query.filter_by(status='todo').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        overdue = Task.query.filter(
            Task.deadline < now,
            Task.status != 'done'
        ).count()
        total_projects = Project.query.count()
        total_members = User.query.filter_by(role='member').count()
        recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    else:
        total_tasks = Task.query.filter_by(assigned_to=current_user['id']).count()
        todo = Task.query.filter_by(assigned_to=current_user['id'], status='todo').count()
        in_progress = Task.query.filter_by(assigned_to=current_user['id'], status='in_progress').count()
        done = Task.query.filter_by(assigned_to=current_user['id'], status='done').count()
        overdue = Task.query.filter(
            Task.assigned_to == current_user['id'],
            Task.deadline < now,
            Task.status != 'done'
        ).count()
        total_projects = len(user.projects)
        total_members = None
        recent_tasks = Task.query.filter_by(
            assigned_to=current_user['id']
        ).order_by(Task.created_at.desc()).limit(5).all()

    response_data = {
        'total_tasks': total_tasks,
        'todo': todo,
        'in_progress': in_progress,
        'done': done,
        'overdue': overdue,
        'total_projects': total_projects,
        'total_members': total_members,
        'recent_tasks': [t.to_dict() for t in recent_tasks],
        'cached': False,
        'cache_status': get_last_cache_status()
    }


    # Store in Redis cache for 5 minutes (300s)
    set_cache(cache_key, response_data, ttl=300)

    return jsonify(response_data), 200