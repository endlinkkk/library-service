from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from contextlib import asynccontextmanager

from application.api.filters import PaginationIn
from domain.entities.library import Borrow as BorrowEntity

from infra.repositories.authors.base import BaseAuthorRepository
from infra.repositories.authors.sqlalchemy_author_repository import (
    SQLAlchemyAuthorRepository,
)
from infra.repositories.books.base import BaseBookRepository
from infra.repositories.borrows.base import BaseBorrowRepository
from logic.exceptions.authors import AuthorNameTooLongException, AuthorNotFoundException

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from logic.exceptions.base import LogicException
from logic.exceptions.books import BookNotFoundException, BookTitleTooLongException
from logic.exceptions.borrows import BorrowReaderNameTooLongException


@dataclass
class BaseBorrowService(ABC):
    @abstractmethod
    async def create_borrow(self, borrow: BorrowEntity) -> BorrowEntity: ...

    # @abstractmethod
    # async def get_borrow_list(self, pagination: PaginationIn) -> Iterable[BorrowEntity]: ...

    # @abstractmethod
    # async def get_borrow(self, borrow_id: int) -> BorrowEntity: ...

    # @abstractmethod
    # async def update_borrow(self, borrow_id: int, borrow: BorrowEntity) -> BorrowEntity: ...

    # @abstractmethod
    # async def delete_borrow(self, borrow_id: int): ...


@dataclass
class BaseBorrowValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        borrow: BorrowEntity,
    ): ...


@dataclass
class BorrowReaderNameValidatorService(BaseBorrowValidatorService):
    def validate(self, borrow: BorrowEntity):
        if len(borrow.reader_name) > 255:
            raise BorrowReaderNameTooLongException(reader_name=borrow.reader_name)


@dataclass
class ComposedBorrowValidatorService:
    validators: list[BaseBorrowValidatorService]

    def validate(self, borrow: BorrowEntity):
        for validator in self.validators:
            validator.validate(borrow=borrow)


@dataclass
class BorrowService(BaseBorrowService):
    session_factory: sessionmaker
    borrow_repository: BaseBorrowRepository

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

    async def create_borrow(self, borrow: BorrowEntity) -> BorrowEntity:
        async with self.get_session() as session:
            saved_borrow = await self.borrow_repository.add(
                borrow=borrow, session=session
            )

        return saved_borrow

    # async def get_book_list(self, pagination: PaginationIn) -> Iterable[BookEntity]:
    #     async with self.get_session() as session:
    #         authors = await self.book_repository.get_all(
    #             session=session, limit=pagination.limit, offset=pagination.offset
    #         )
    #     return authors

    # async def get_book(self, book_id: int) -> BookEntity | None:
    #     async with self.get_session() as session:
    #         book = await self.book_repository.get_by_id(
    #             book_id=book_id, session=session
    #         )

    #     if book is None:
    #         raise BookNotFoundException()

    #     return book

    # async def update_book(self, book_id: int, book: BookEntity) -> BookEntity:
    #     async with self.get_session() as session:
    #         book = await self.book_repository.update(
    #             book_id=book_id, session=session, book=book
    #         )

    #         await session.commit()

    #     if book is None:
    #         raise BookNotFoundException()

    #     return book

    # async def delete_book(self, book_id: int):
    #     async with self.get_session() as session:
    #         deleted = await self.book_repository.delete(
    #             book_id=book_id, session=session
    #         )
    #         await session.commit()

    #     if not deleted:
    #         raise BookNotFoundException()
