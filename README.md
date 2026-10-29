# Bookstore CRUD API

FastAPI + SQLAlchemy 2.0 + PostgreSQL + Docker Compose.

## Run with Docker (API + database)

```bash
cp .env.example .env        # Windows: copy .env.example .env
docker compose up --build
```

- API:     http://localhost:8000
- Swagger: http://localhost:8000/docs

## Run locally (venv)

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
docker compose up -d db           # start only PostgreSQL
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```
