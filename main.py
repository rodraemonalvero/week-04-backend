from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import Book
from schemas import BookCreate, BookUpdate, BookResponse

# Create tables in the database if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Tracker API", version="2.0.0")

# Pydantic models for validation
class BookCreate(BaseModel):
    title: str
    author: str
    status: str = "want_to_read"  # "reading", "read", "want_to_read"
    rating: Optional[int] = None  # 1-5, only if status is "read"

class BookUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[int] = None

# In-memory storage
books_db = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to Book Tracker API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books")
def get_books(status: Optional[str] = None):
    if status:
        return [b for b in books_db if b["status"] == status]
    return books_db


@app.get("/books/stats")
def get_stats():
    total = len(books_db)

    reading = len([
        b for b in books_db
        if b["status"] == "reading"
    ])

    read = len([
        b for b in books_db
        if b["status"] == "read"
    ])

    want_to_read = len([
        b for b in books_db
        if b["status"] == "want_to_read"
    ])

    read_books = [
        b for b in books_db
        if b["status"] == "read" and b["rating"] is not None
    ]

    if len(read_books) > 0:
        average_rating = sum(
            b["rating"] for b in read_books
        ) / len(read_books)
    else:
        average_rating = 0

    return {
        "total_books": total,
        "reading": reading,
        "read": read,
        "want_to_read": want_to_read,
        "average_rating": average_rating
    }


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_id

    new_book = book.model_dump()
    new_book["id"] = next_id

    books_db.append(new_book)
    next_id += 1

    return new_book


@app.put("/books/{book_id}")
def update_book(book_id: int, updates: BookUpdate):
    for book in books_db:
        if book["id"] == book_id:
            if updates.status is not None:
                book["status"] = updates.status

            if updates.rating is not None:
                book["rating"] = updates.rating

            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            books_db.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")