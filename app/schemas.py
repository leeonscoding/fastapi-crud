from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    isbn: str = Field(min_length=10, max_length=20, examples=["9780132350884"])
    published_year: int | None = Field(default=None, ge=1000, le=2100)


class BookCreate(BookBase):
    """Payload for POST and PUT (full replacement)."""


class BookUpdate(BaseModel):
    """Payload for PATCH: every field is optional."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=120)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)
    published_year: int | None = Field(default=None, ge=1000, le=2100)


class BookRead(BookBase):
    """Response model. from_attributes lets Pydantic read SQLAlchemy objects."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
