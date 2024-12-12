from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(eq=False)
class Book:
    title: str
    description: str
    author_id: int
    available_copies: int
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime | None = field(default=None)


@dataclass(eq=False)
class Author:
    name: str
    surname: str
    date_of_birth: date
    books: set[Book] = field(default_factory=set, kw_only=True)
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime | None = field(default=None)


@dataclass(eq=False)
class Borrow:
    book_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: datetime | None = None
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime | None = field(default=None)
