from pydantic import BaseModel
from typing import List, Optional

# Base schema for Author
class AuthorBase(BaseModel):
    name: str
    birthdate: Optional[str] = None

# Schema for creating an author
class AuthorCreate(AuthorBase):
    pass

# Schema for updating an author
class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[str] = None

# Schema for reading an author
class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# Base schema for Book
class BookBase(BaseModel):
    title: str
    author_id: int
    publication_date: Optional[str] = None

# Schema for creating a book
class BookCreate(BookBase):
    pass

# Schema for updating a book
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    publication_date: Optional[str] = None

# Schema for reading a book
class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

# Optional: Schema for paginated responses
class PaginatedAuthors(BaseModel):
    authors: List[Author]
    total: int

class PaginatedBooks(BaseModel):
    books: List[Book]
    total: int
