from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

DbSession = Annotated[Session, Depends(get_db)]


def get_book_or_404(book_id: int, db: DbSession) -> Book:
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Book {book_id} not found")
    return book


def ensure_isbn_available(db: Session, isbn: str, current_id: int | None = None) -> None:
    existing = crud.get_book_by_isbn(db, isbn)
    if existing is not None and existing.id != current_id:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"A book with ISBN {isbn} already exists"
        )


@router.get("", response_model=list[BookRead])
def list_books(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return crud.list_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookRead)
def read_book(book: Annotated[Book, Depends(get_book_or_404)]):
    return book  # SQLAlchemy object -> BookRead (via from_attributes)


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: DbSession):
    ensure_isbn_available(db, payload.isbn)
    return crud.create_book(db, payload)


@router.put("/{book_id}", response_model=BookRead)
def replace_book(
    payload: BookCreate,
    book: Annotated[Book, Depends(get_book_or_404)],
    db: DbSession,
):
    ensure_isbn_available(db, payload.isbn, current_id=book.id)
    return crud.replace_book(db, book, payload)


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    payload: BookUpdate,
    book: Annotated[Book, Depends(get_book_or_404)],
    db: DbSession,
):
    if payload.isbn is not None:
        ensure_isbn_available(db, payload.isbn, current_id=book.id)
    return crud.update_book(db, book, payload)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book: Annotated[Book, Depends(get_book_or_404)],
    db: DbSession,
):
    crud.delete_book(db, book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
