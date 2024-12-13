from datetime import datetime
from pydantic import BaseModel

from domain.entities.library import Book as BookEntity


class InBookSchema(BaseModel):
    title: str
    description: str
    author_id: int
    available_copies: int = 1

    def to_entity(self) -> BookEntity:
        return BookEntity(
            title=self.title,
            description=self.description,
            author_id=self.author_id,
            available_copies=self.available_copies,
        )


class OutBookSchema(BaseModel):
    id: int
    title: str
    description: str
    author_id: int
    available_copies: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(book: BookEntity) -> "OutBookSchema":
        return OutBookSchema(
            id=book.id,
            title=book.title,
            description=book.description,
            author_id=book.author_id,
            available_copies=book.available_copies,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )


BookListSchema = list[OutBookSchema]
