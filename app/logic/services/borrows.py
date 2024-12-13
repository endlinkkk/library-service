from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from contextlib import asynccontextmanager

from application.api.filters import PaginationIn
from domain.entities.library import Borrow as BorrowEntity


from infra.repositories.borrows.base import BaseBorrowRepository


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


from logic.exceptions.borrows import (
    BorrowNotFoundException,
    BorrowReaderNameTooLongException,
)


@dataclass
class BaseBorrowService(ABC):
    @abstractmethod
    async def create_borrow(self, borrow: BorrowEntity) -> BorrowEntity: ...

    @abstractmethod
    async def get_borrow_list(
        self, pagination: PaginationIn
    ) -> Iterable[BorrowEntity]: ...

    @abstractmethod
    async def get_borrow(self, borrow_id: int) -> BorrowEntity: ...

    @abstractmethod
    async def completion_of_the_issue(self, borrow_id: int) -> BorrowEntity: ...


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

    async def get_borrow_list(self, pagination: PaginationIn) -> Iterable[BorrowEntity]:
        async with self.get_session() as session:
            authors = await self.borrow_repository.get_all(
                session=session, limit=pagination.limit, offset=pagination.offset
            )
        return authors

    async def get_borrow(self, borrow_id: int) -> BorrowEntity | None:
        async with self.get_session() as session:
            borrow = await self.borrow_repository.get_by_id(
                borrow_id=borrow_id, session=session
            )

            if borrow is None:
                raise BorrowNotFoundException()

        return borrow

    async def completion_of_the_issue(self, borrow_id: int) -> BorrowEntity:
        async with self.get_session() as session:
            borrow = await self.borrow_repository.completion_issue(
                session=session, borrow_id=borrow_id
            )

            if borrow is None:
                raise BorrowNotFoundException()

        return borrow
