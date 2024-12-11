from sqlalchemy.orm import Session
from sqlalchemy.future import select

from domain.entities.library import Author as AuthorEntity
from infra.database.models import AuthorModel
from infra.repositories.authors.base import BaseAuthorRepository
from dataclasses import dataclass


@dataclass
class SQLAlchemyAuthorRepository(BaseAuthorRepository):
    session: Session

    async def add(self, author: AuthorEntity) -> AuthorEntity:
        author_model = AuthorModel(
            name=author.name, surname=author.surname, date_of_birth=author.date_of_birth
        )
        self.session.add(author_model)
        await self.session.flush()  # Flush to get the ID
        return AuthorEntity(
            id=author_model.id,
            name=author_model.name,
            surname=author_model.surname,
            date_of_birth=author_model.date_of_birth,
            created_at=author_model.created_at,
            updated_at=author_model.updated_at,
        )

    # def get_by_id(self, author_id: int) -> Optional[AuthorEntity]:
    #     author_model = self.session.query(AuthorModel).filter_by(id=author_id).first()
    #     if author_model:
    #         return AuthorEntity(
    #             id=author_model.id,
    #             name=author_model.name,
    #             surname=author_model.surname,
    #             date_of_birth=author_model.date_of_birth
    #         )
    #     return None

    async def get(self, limit: int = 20, offset: int = 0) -> list[AuthorEntity]:
        result = await self.session.execute(
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

    # def update(self, author: AuthorEntity) -> AuthorEntity:
    #     author_model = self.session.query(AuthorModel).filter_by(id=author.id).first()
    #     if author_model:
    #         author_model.name = author.name
    #         author_model.surname = author.surname
    #         author_model.date_of_birth = author.date_of_birth
    #         self.session.flush()
    #         return Author(
    #             id=author_model.id,
    #             name=author_model.name,
    #             surname=author_model.surname,
    #             date_of_birth=author_model.date_of_birth
    #         )
    #     return None

    # def delete(self, author_id: int) -> None:
    #     author_model = self.session.query(AuthorModel).filter_by(id=author_id).first()
    #     if author_model:
    #         self.session.delete(author_model)
    #         self.session.flush()
