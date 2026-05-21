from datetime import datetime, timezone
from models import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='todo')  # todo / in_progress / done
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low / medium / high
    deadline = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'project_id': self.project_id,
            'assigned_to': self.assigned_to,
            'assignee_name': self.assignee.name if self.assignee else None,
            'created_at': self.created_at.isoformat()
        }