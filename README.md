# Andiny Atlas

Andiny Atlas is an Operational Intelligence Platform designed to assist support engineers in diagnosing, investigating, and resolving technical cases through structured workflows and intelligent decision-making.

## Vision

Atlas aims to become an enterprise-grade operational platform capable of:

- Automating technical investigations
- Standardizing troubleshooting workflows
- Integrating with external platforms and APIs
- Maintaining complete investigation history
- Providing AI-assisted operational recommendations

---

## Current Capabilities (Sprint 1)

- FastAPI backend
- Health monitoring endpoint
- Support investigation API
- Workflow-based decision engine
- Swagger/OpenAPI documentation
- Git version control

---

## Project Structure

```
andiny-atlas/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   │
│   └── venv/
│
├── .gitignore
├── README.md
└── backend/requirements.txt
```

---

## Running Atlas

Create and activate a virtual environment.

Install dependencies:

```
pip install -r backend/requirements.txt
```

Start the server:

```
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Roadmap

### Sprint 1 ✅
- Backend foundation
- Investigation engine
- API endpoints
- Git repository

### Sprint 2 🚧
- Case IDs
- Investigation history
- Logging
- Documentation

### Sprint 3
- Database integration
- Case search
- Persistent storage

### Sprint 4
- Authentication
- User accounts
- Role-based permissions

### Sprint 5
- Operational dashboard

### Sprint 6
- External integrations
- Samsung Knox
- Intelligra APIs

### Sprint 7
- AI-assisted investigations
- Intelligent recommendations
- Operational analytics

---

## Author

Developed by Dallas Uzo.

Project: **Andiny Atlas**