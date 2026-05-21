from datetime import datetime, timezone
from models import db

project_members = db.Table('project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    members = db.relationship('User', secondary=project_members, lazy='subquery',
                backref=db.backref('projects', lazy=True))
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'members': [{'id': m.id, 'name': m.name, 'email': m.email} for m in self.members]
        }