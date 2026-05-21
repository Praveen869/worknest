# 🪺 WorkNest — Team Task Manager

WorkNest is a lightweight, self-hostable team task management application built with Flask and PostgreSQL. It provides user authentication, project and task management, role-based access, and a simple dashboard for tracking progress.

## Table of contents

- Project overview
- Features
- Tech stack
- Architecture
- Getting started (local development)
- Environment variables
- Running the app
- Testing
- Deployment
- Contributing
- Security & secrets
- License

## Project overview

WorkNest helps small teams plan, assign, and track tasks inside projects. It aims to be simple to deploy and easy to extend.

## Features

- JWT-based authentication (signup, login)
- Role-based access control (admin and member)
- Project creation and team membership
- Task creation, assignment, comments, and status updates
- Dashboard with basic statistics and overdue task alerts

## Tech stack

- Backend: Flask, SQLAlchemy, Flask-JWT-Extended
- Database: PostgreSQL
- Frontend: Server-rendered HTML templates, CSS, Vanilla JavaScript
- Migrations: Flask-Migrate (Alembic)

## Architecture

The repository follows a simple separation:

- `backend/`: Flask application, models, routes, and configuration
- `frontend/`: static assets and Jinja2 templates

## Getting started (local development)

Prerequisites

- Python 3.10+ (recommended)
- PostgreSQL (local or remote)

Quickstart

1. Clone the repository

```bash
git clone <your-repo-url>
cd worknest
```

2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

4. Copy environment example and set secrets

```bash
copy backend\.env.example backend\.env
# then edit backend\.env and fill real values
```

5. Initialize the database (example using Flask-Migrate)

```bash
set FLASK_APP=backend/app.py
flask db upgrade
```

## Environment variables

Copy `backend/.env.example` to `backend/.env` and fill the values. Example variables include:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname
JWT_SECRET_KEY=your-jwt-secret
DEBUG=False
```

Do not commit the real `backend/.env` file. The repository includes `backend/.env.example` to document required variables.

## Running the app

Run the Flask application for local development:

```powershell
venv\Scripts\activate
cd backend
python app.py
```

Open your browser at `http://127.0.0.1:5000` (or the configured host/port).

## Testing

If there are unit or integration tests, run them from the project root. Example (pytest):

```bash
pip install pytest
pytest
```

If you want, I can add a CI workflow to run tests on push.

## Deployment

WorkNest is suitable for simple deployments (Railway, Render, Heroku). Key things to configure in production:

- Set `DATABASE_URL` to a managed Postgres instance
- Set `SECRET_KEY` and `JWT_SECRET_KEY` to strong, random values
- Set `DEBUG=False`

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch
3. Add tests for new behavior
4. Open a pull request with a clear description

## Security & secrets

- Do not commit credentials or `.env` files. `.gitignore` already excludes them.
- Rotate any leaked keys immediately.
- Use `backend/.env.example` to share the list of env variables without exposing secrets.

## License

This project is published under the [MIT License](LICENSE).

## Contact

If you need help or want me to: set up CI, add a GitHub Actions workflow, or prepare the repository for deployment, tell me and I'll prepare it.


Copy `backend/.env.example` to `backend/.env` and fill in your secrets:

```
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
DEBUG=False
```

**Never commit your real `.env` file!**

## GitHub Safety & Best Practices

- Sensitive data (secrets, API keys, DB URLs) must go in `.env` (never commit real secrets)
- `.gitignore` is set up to hide `.env`, venv, and system files
- Use `backend/.env.example` to share required environment variables
- Review code for hardcoded secrets before pushing

## License

This project is licensed under the [MIT License](LICENSE).