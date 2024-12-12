from sqlalchemy.orm import Session
from sqlalchemy.future import select

from domain.entities.library import Author as AuthorEntity
from infra.database.models import AuthorModel
from infra.repositories.authors.base import BaseAuthorRepository
from dataclasses import dataclass


@dataclass
class SQLAlchemyAuthorRepository(BaseAuthorRepository):

    async def add(self, author: AuthorEntity, session: Session) -> AuthorEntity:
        author_model = AuthorModel(
            name=author.name, surname=author.surname, date_of_birth=author.date_of_birth
        )
        session.add(author_model)
        await session.flush()
        return AuthorEntity(
            id=author_model.id,
            name=author_model.name,
            surname=author_model.surname,
            date_of_birth=author_model.date_of_birth,
            created_at=author_model.created_at,
            updated_at=author_model.updated_at,
        )

    async def get_by_id(self, author_id: int, session: Session) -> AuthorEntity | None:
        result = await session.execute(
            select(AuthorModel).where(AuthorModel.id == author_id)
        )
        author_model = result.scalars().one_or_none()
        if author_model:
            return AuthorEntity(
                id=author_model.id,
                name=author_model.name,
                surname=author_model.surname,
                date_of_birth=author_model.date_of_birth,
                created_at=author_model.created_at,
                updated_at=author_model.updated_at,
            )

    async def get_all(self, session: Session, limit: int = 20, offset: int = 0) -> list[AuthorEntity]:
        result = await session.execute(
            select(AuthorModel).offset(offset).limit(limit)
        )
        author_models = result.scalars().all()
        return [
            AuthorEntity(
                id=author_model.id,
                name=author_model.name,
                surname=author_model.surname,
                date_of_birth=author_model.date_of_birth,
                created_at=author_model.created_at,
                updated_at=author_model.updated_at,
            )
            for author_model in author_models
        ]

    async def update(self, session: Session, author_id: int, author: AuthorEntity) -> AuthorEntity | None:
        result = await session.execute(
            select(AuthorModel).where(AuthorModel.id == author_id)
        )
        author_model = result.scalars().one_or_none()

        if author_model:
            author_model.name = author.name
            author_model.surname = author.surname
            author_model.date_of_birth = author.date_of_birth
            session.flush()
            return AuthorEntity(
                id=author_model.id,
                name=author_model.name,
                surname=author_model.surname,
                date_of_birth=author_model.date_of_birth,
                created_at=author_model.created_at,
                updated_at=author_model.updated_at,
            )
        return None
    

    async def delete(self, session: Session, author_id: int) -> bool:
        result = await session.execute(
            select(AuthorModel).where(AuthorModel.id == author_id)
        )
        author_model = result.scalars().one_or_none()
        if author_model:
            await session.delete(author_model)
            await session.flush()
            return True
        return False


