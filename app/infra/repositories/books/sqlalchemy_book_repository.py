from sqlalchemy.orm import Session
from sqlalchemy.future import select


from domain.entities.library import Book as BookEntity

from infra.database.models import BookModel
from dataclasses import dataclass

from infra.repositories.books.base import BaseBookRepository


@dataclass
class SQLAlchemyBookRepository(BaseBookRepository):
    async def add(self, book: BookEntity, session: Session) -> BookEntity:
        book_model = BookModel(
            title=book.title,
            description=book.description,
            author_id=book.author_id,
            available_copies=book.available_copies,
        )
        session.add(book_model)
        await session.flush()
        return BookEntity(
            id=book_model.id,
            title=book_model.title,
            description=book_model.description,
            author_id=book_model.author_id,
            available_copies=book_model.available_copies,
            created_at=book_model.created_at,
            updated_at=book_model.updated_at,
        )

    async def get_by_id(self, book_id: int, session: Session) -> BookEntity | None:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book_model = result.scalars().one_or_none()
        if book_model:
            return BookEntity(
                id=book_model.id,
                title=book_model.title,
                description=book_model.description,
                author_id=book_model.author_id,
                available_copies=book_model.available_copies,
                created_at=book_model.created_at,
                updated_at=book_model.updated_at,
            )

    async def get_all(
        self, session: Session, limit: int = 20, offset: int = 0
    ) -> list[BookEntity]:
        result = await session.execute(select(BookModel).offset(offset).limit(limit))
        book_models = result.scalars().all()
        return [
            BookEntity(
                id=book_model.id,
                title=book_model.title,
                description=book_model.description,
                author_id=book_model.author_id,
                available_copies=book_model.available_copies,
                created_at=book_model.created_at,
                updated_at=book_model.updated_at,
            )
            for book_model in book_models
        ]

    async def update(
        self, session: Session, book_id: int, book: BookEntity
    ) -> BookEntity | None:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book_model = result.scalars().one_or_none()

        if book_model:
            book_model.title = book.title
            book_model.description = book.description
            book_model.available_copies = book.available_copies
            book_model.author_id = book.author_id
            session.flush()
            return BookEntity(
                id=book_model.id,
                title=book_model.title,
                description=book_model.description,
                author_id=book_model.author_id,
                available_copies=book_model.available_copies,
                created_at=book_model.created_at,
                updated_at=book_model.updated_at,
            )
        return None

    async def delete(self, session: Session, book_id: int) -> bool:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book_model = result.scalars().one_or_none()
        if book_model:
            await session.delete(book_model)
            await session.flush()
            return True
        return False

    async def reduce_by_one(self, session: Session, book_id: int) -> bool:
        result = await session.execute(select(BookModel).where(BookModel.id == book_id))
        book_model: BookModel = result.scalars().one_or_none()
        if book_model and book_model.available_copies >= 1:
            book_model.available_copies -= 1
            await session.flush()
            return True
        return False
