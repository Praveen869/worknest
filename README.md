# 🪺 WorkNest — Team Task & Project Management Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Cache-Redis-red.svg)](https://redis.io/)
[![JWT](https://img.shields.io/badge/Auth-JWT_Tokens-orange.svg)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

WorkNest is a production-ready, self-hostable team task management platform. It features stateless JWT authentication, fine-grained Role-Based Access Control (RBAC), Redis-cached dashboard analytics, and PostgreSQL database management.

---

## 🌟 Key Features

- **Stateless JWT Authentication:** Secure registration & login flow with JWT token lifecycle management.
- **Role-Based Access Control (RBAC):** Admin and Member role isolation for project management and task assignment.
- **High-Performance Redis Caching:** In-memory caching for analytical dashboard queries (`<20ms` latency) with automatic cache invalidation on task mutations.
- **Project & Task Lifecycle Management:** Full CRUD operations for projects, team memberships, deadlines, and task progress tracking (`todo`, `in_progress`, `done`).
- **Interactive Dashboards:** Real-time task statistics, member assignment views, and automated overdue task alerts.
- **Database Migrations:** Managed schema migrations using Flask-Migrate (Alembic) and SQLAlchemy ORM.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10, Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Caching & Latency:** Redis (`redis-py`) with fallback to database queries
- **Database:** PostgreSQL (with `pg8000` / `psycopg2` driver support)
- **Frontend:** Server-rendered HTML templates (Jinja2), Custom Vanilla CSS, Modern JavaScript (ES6+)
- **Server & Deployment:** Gunicorn WSGI web server, Docker-ready, GitHub Actions CI

---

## 📂 Architecture & Directory Structure

```
worknest/
├── backend/
│   ├── app.py              # Main Flask application entrypoint & extension bindings
│   ├── cache.py            # Redis cache manager & graceful fallback logic
│   ├── config.py           # Application configuration & env loader
│   ├── models/             # SQLAlchemy ORM schemas (User, Project, Task)
│   ├── routes/             # RESTful API Endpoints (auth, projects, tasks, dashboard)
│   └── requirements.txt    # Python backend dependencies
├── frontend/
│   ├── static/             # Static CSS styles and JavaScript scripts
│   └── templates/          # Jinja2 HTML views (Dashboard, Projects, Login)
├── .github/workflows/      # GitHub Actions CI workflow
├── Procfile                # Gunicorn deployment config
└── README.md               # Documentation
```

---

## 🚀 Getting Started (Local Development)

### Prerequisites

- **Python 3.10+**
- **PostgreSQL** (Local or Managed Remote Instance e.g., Railway/Render)
- **Redis Server** (Optional for caching, defaults to graceful fallback if unavailable)

### Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/worknest.git
   cd worknest
   ```

2. **Create and activate virtual environment:**
   ```powershell
   # Windows PowerShell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Setup Environment Variables:**
   Copy `backend/.env.example` to `backend/.env` and update values:
   ```env
   SECRET_KEY=your-strong-secret-key
   DATABASE_URL=postgresql://user:pass@localhost:5432/worknest_db
   JWT_SECRET_KEY=your-jwt-secret-key
   REDIS_URL=redis://localhost:6379/0
   DEBUG=True
   ```

5. **Initialize Database & Run App:**
   ```bash
   cd backend
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

---

## 🔒 Security & Best Practices

- **Zero Hardcoded Secrets:** All secrets, keys, and connection strings are managed via `.env`.
- **Git Safety:** `.gitignore` excludes local environment configs, virtual environments (`venv/`), and cached build files.
- **RBAC Decorators:** Custom permission wrappers protect administrative endpoints from member escalation.

---

## 📄 License

Published under the [MIT License](LICENSE).