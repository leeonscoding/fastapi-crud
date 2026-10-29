from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registers models on Base.metadata)
from app.database import Base, engine
from app.routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fine for a tutorial. In production, use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Bookstore CRUD API",
    description="A CRUD API built with FastAPI, SQLAlchemy 2.0 and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(books.router)


@app.get("/", tags=["root"])
def hello_world():
    return {"message": "Hello, World!"}


@app.get("/health", tags=["root"])
def health():
    return {"status": "ok"}
