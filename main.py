from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import Book
from schemas import BookCreate, BookUpdate, BookResponse

# Create tables in the database if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Tracker API", version="2.0.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to Book Tracker API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books", response_model=list[BookResponse])
def get_books(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)

    if status:
        query = query.filter(Book.status == status)

    return query.all()


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


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**data.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = updates.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}