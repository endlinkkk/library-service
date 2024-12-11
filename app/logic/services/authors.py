from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from contextlib import asynccontextmanager

from application.api.filters import PaginationIn
from domain.entities.library import Author as AuthorEntity

from infra.repositories.authors.base import BaseAuthorRepository
from infra.repositories.authors.sqlalchemy_author_repository import (
    SQLAlchemyAuthorRepository,
)
from logic.exceptions.authors import AuthorNameTooLongException

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


@dataclass
class BaseAuthorService(ABC):
    @abstractmethod
    async def get_author_list(self, pagination: PaginationIn) -> Iterable[AuthorEntity]:
        ...

    @abstractmethod
    async def create_author(self, author: AuthorEntity) -> AuthorEntity: ...


@dataclass
class BaseAuthorValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        author: AuthorEntity,
    ): ...


@dataclass
class AuthorNameValidatorService(BaseAuthorValidatorService):
    def validate(self, author: AuthorEntity):
        if len(author.name) > 255:
            raise AuthorNameTooLongException(name=author.name)


@dataclass
class AuthorService(BaseAuthorService):
    session_factory: sessionmaker

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            session: AsyncSession = self.session_factory()
            yield session

        finally:
            await session.close()

    async def create_author(self, author: AuthorEntity) -> AuthorEntity:
        async with self.get_session() as session:
            author_repository = SQLAlchemyAuthorRepository(session=session)
            saved_author = await author_repository.add(author)
            await session.commit()

        return saved_author
    

    async def get_author_list(self, pagination: PaginationIn) -> Iterable[AuthorEntity]:
        async with self.get_session() as session:
            author_repository = SQLAlchemyAuthorRepository(session=session)
            authors = await author_repository.get(limit=pagination.limit, offset=pagination.offset)
        return authors
