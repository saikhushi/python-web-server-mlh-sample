# Notesy — Simple Notes Web App (MLH-style code sample)

**What it is:** A small, deployable Flask web server that provides user authentication (JWT),
a REST API for creating/reading/updating/deleting personal notes, and a minimal frontend
to demonstrate usage. Intended as a representative code sample for MLH Fellowship apps.

**Tech stack:** Python, Flask, Flask_SQLAlchemy, Flask-JWT-Extended, SQLite, vanilla JS

## Files
- `app.py` — application factory & run entrypoint
- `models.py` — SQLAlchemy models (User, Note)
- `auth.py` — authentication helper routes (register / login) using JWT
- `routes.py` — API routes for notes CRUD (protected)
- `templates/index.html` — minimal frontend UI
- `static/app.js` — frontend logic (fetch API)
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Quick start (local)
1. Create and activate a virtualenv (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run --host=0.0.0.0 --port=5000
   ```
   Or simply: `python app.py`
4. Open `http://localhost:5000` in your browser. Register, login, and create notes.

## Notes about this sample
- Uses SQLite for simplicity; replace with PostgreSQL/MySQL for production.
- JWT used for stateless authentication (suitable for SRE/production-like setups).
- Frontend is intentionally minimal — focus is on backend code you can discuss in interviews.
