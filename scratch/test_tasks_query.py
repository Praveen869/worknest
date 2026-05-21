import sys
sys.path.append('backend')
from app import app
from models import db
from models.user import User
from models.task import Task
from models.project import Project

with app.app_context():
    print("=== USERS ===")
    for u in User.query.all():
        print(f"ID: {u.id}, Name: {u.name}, Email: {u.email}, Role: {u.role}")

    print("\n=== PROJECTS ===")
    for p in Project.query.all():
        members_str = ", ".join([f"{m.name} (ID: {m.id})" for m in p.members])
        print(f"ID: {p.id}, Name: {p.name}, Owner ID: {p.owner_id}, Members: [{members_str}]")

    print("\n=== TASKS ===")
    for t in Task.query.all():
        print(f"ID: {t.id}, Title: {t.title}, Project ID: {t.project_id}, Assigned To: {t.assigned_to}")

    print("\n=== TESTING QUERIES FOR EACH USER ===")
    for u in User.query.all():
        print(f"\nUser: {u.name} (Role: {u.role})")
        # 1. Under "All Projects" - Current backend logic:
        # tasks = Task.query.filter_by(assigned_to=u.id).all()
        tasks_all_proj = Task.query.filter_by(assigned_to=u.id).all()
        print(f"  All Projects (Current): {[t.id for t in tasks_all_proj]}")
        
        # 2. Under a specific Project 2 - Current backend logic:
        # tasks = Task.query.filter_by(assigned_to=u.id, project_id=2).all()
        tasks_proj2 = Task.query.filter_by(assigned_to=u.id, project_id=2).all()
        print(f"  Project 2 (Current): {[t.id for t in tasks_proj2]}")

        # 3. Under "All Projects" - Proposed backend logic (all tasks in their projects):
        project_ids = [p.id for p in u.projects]
        tasks_proposed = Task.query.filter(Task.project_id.in_(project_ids)).all() if project_ids else []
        print(f"  All Projects (Proposed): {[t.id for t in tasks_proposed]}")
