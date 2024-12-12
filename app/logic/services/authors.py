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
from logic.exceptions.authors import AuthorNameTooLongException, AuthorNotFoundException

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from logic.exceptions.base import LogicException


@dataclass
class BaseAuthorService(ABC):
    @abstractmethod
    async def get_author_list(self, pagination: PaginationIn) -> Iterable[AuthorEntity]:
        ...

    @abstractmethod
    async def create_author(self, author: AuthorEntity) -> AuthorEntity: ...

    @abstractmethod
    async def get_author(self, author_id: int) -> AuthorEntity: ...

    @abstractmethod
    async def update_author(self, author_id: int, author: AuthorEntity) -> AuthorEntity: ...

    @abstractmethod
    async def delete_author(self, author_id: int): ...


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
class ComposedAuthorValidatorService:
    validators: list[BaseAuthorValidatorService]

    def validate(
            self,
            author: AuthorEntity
    ):
        for validator in self.validators:
            validator.validate(author=author)


@dataclass
class AuthorService(BaseAuthorService):
    session_factory: sessionmaker
    author_repository: BaseAuthorRepository

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            session: AsyncSession = self.session_factory()
            yield session

        finally:
            await session.close()

    async def create_author(self, author: AuthorEntity) -> AuthorEntity:
        async with self.get_session() as session:
            saved_author = await self.author_repository.add(author=author, session=session)
            await session.commit()

        return saved_author
    

    async def get_author_list(self, pagination: PaginationIn) -> Iterable[AuthorEntity]:
        async with self.get_session() as session:
            authors = await self.author_repository.get_all(session=session, limit=pagination.limit, offset=pagination.offset)
        return authors
    

    async def get_author(self, author_id: int) -> AuthorEntity:
        async with self.get_session() as session:
            author = await self.author_repository.get_by_id(author_id=author_id, session=session)

        if author is None:
            raise AuthorNotFoundException()
        
        
        return author


    async def update_author(self, author_id: int, author: AuthorEntity) -> AuthorEntity:
        async with self.get_session() as session:
            author = await self.author_repository.update(author_id=author_id, session=session, author=author)

            await session.commit()
        
        if author is None:
            raise AuthorNotFoundException()
        
        return author
    
    async def delete_author(self, author_id: int):
        async with self.get_session() as session:
            deleted = await self.author_repository.delete(author_id=author_id, session=session)
            await session.commit()
        
        if not deleted:
            raise AuthorNotFoundException()
        