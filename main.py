from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import session
from typing import List

import crud
import models
import schemas
from database import SessionLocal, engine

# Creating the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creating an author
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

# Reading authors
@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

# Update Author
def update_author(db: session, author: models.Author, author_update: schemas.AuthorUpdate):
    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author

# Delete Author
def delete_author(db: session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author:
        db.delete(author)
        db.commit()
    return author


# Create a book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: session = Depends(get_db)):
    author = crud.get_author(db, author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return crud.create_book(db=db, book=book)

#Read a book
@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Update Book
def update_book(db: session, book: models.Book, book_update: schemas.BookUpdate):
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# Delete Book
def delete_book(db: session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book
