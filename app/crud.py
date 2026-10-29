from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Book
from app.schemas import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def get_book_by_isbn(db: Session, isbn: str) -> Book | None:
    return db.scalars(select(Book).where(Book.isbn == isbn)).first()


def list_books(db: Session, skip: int = 0, limit: int = 10) -> list[Book]:
    stmt = select(Book).order_by(Book.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_book(db: Session, payload: BookCreate) -> Book:
    # Pydantic -> SQLAlchemy
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def replace_book(db: Session, book: Book, payload: BookCreate) -> Book:
    for field, value in payload.model_dump().items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book: Book, payload: BookUpdate) -> Book:
    # exclude_unset => only touch fields the client actually sent
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
