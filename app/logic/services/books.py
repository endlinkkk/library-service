from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from contextlib import asynccontextmanager

from application.api.filters import PaginationIn
from domain.entities.library import Book as BookEntity


from infra.repositories.books.base import BaseBookRepository


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from logic.exceptions.books import (
    BookIsNotAvailableException,
    BookNotFoundException,
    BookTitleTooLongException,
)


@dataclass
class BaseBookService(ABC):
    @abstractmethod
    async def create_book(self, book: BookEntity) -> BookEntity: ...

    @abstractmethod
    async def get_book_list(self, pagination: PaginationIn) -> Iterable[BookEntity]: ...

    @abstractmethod
    async def get_book(self, book_id: int) -> BookEntity: ...

    @abstractmethod
    async def update_book(self, book_id: int, book: BookEntity) -> BookEntity: ...

    @abstractmethod
    async def delete_book(self, book_id: int): ...

    @abstractmethod
    async def reduce_the_quantity_by_one(self, book_id: int): ...

    @abstractmethod
    async def increase_the_quantity_by_one(self, nook_id: int): ...


@dataclass
class BaseBookValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        book: BookEntity,
    ): ...


@dataclass
class BookTitleValidatorService(BaseBookValidatorService):
    def validate(self, book: BookEntity):
        if len(book.title) > 255:
            raise BookTitleTooLongException(title=book.title)


@dataclass
class ComposedBookValidatorService:
    validators: list[BaseBookValidatorService]

    def validate(self, book: BookEntity):
        for validator in self.validators:
            validator.validate(book=book)


@dataclass
class BookService(BaseBookService):
    session_factory: sessionmaker
    book_repository: BaseBookRepository

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            session: AsyncSession = self.session_factory()
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()

    async def create_book(self, book: BookEntity) -> BookEntity:
        async with self.get_session() as session:
            saved_book = await self.book_repository.add(book=book, session=session)

        return saved_book

    async def get_book_list(self, pagination: PaginationIn) -> Iterable[BookEntity]:
        async with self.get_session() as session:
            authors = await self.book_repository.get_all(
                session=session, limit=pagination.limit, offset=pagination.offset
            )
        return authors

    async def get_book(self, book_id: int) -> BookEntity | None:
        async with self.get_session() as session:
            book = await self.book_repository.get_by_id(
                book_id=book_id, session=session
            )

            if book is None:
                raise BookNotFoundException()

        return book

    async def update_book(self, book_id: int, book: BookEntity) -> BookEntity:
        async with self.get_session() as session:
            book = await self.book_repository.update(
                book_id=book_id, session=session, book=book
            )

            if book is None:
                raise BookNotFoundException()

        return book

    async def delete_book(self, book_id: int):
        async with self.get_session() as session:
            deleted = await self.book_repository.delete(
                book_id=book_id, session=session
            )

            if not deleted:
                raise BookNotFoundException()

    async def reduce_the_quantity_by_one(self, book_id: int):
        async with self.get_session() as session:
            decreased = await self.book_repository.reduce_by_one(
                book_id=book_id, session=session
            )
            if not decreased:
                raise BookIsNotAvailableException()

    async def increase_the_quantity_by_one(self, book_id: int):
        async with self.get_session() as session:
            increased = await self.book_repository.increase_by_one(
                book_id=book_id, session=session
            )
            if not increased:
                raise BookNotFoundException()
