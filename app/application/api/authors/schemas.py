from datetime import date
from pydantic import BaseModel
from datetime import datetime

from domain.entities.library import Author as AuthorEntity


class InAuthorSchema(BaseModel):
    name: str
    surname: str
    date_of_birth: date

    def to_entity(self) -> AuthorEntity:
        return AuthorEntity(
            name=self.name, surname=self.surname, date_of_birth=self.date_of_birth
        )


class OutAuthorSchema(BaseModel):
    id: int
    name: str
    surname: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: AuthorEntity) -> "OutAuthorSchema":
        return OutAuthorSchema(
            id=entity.id,
            name=entity.name,
            surname=entity.surname,
            date_of_birth=entity.date_of_birth,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


AuthorListSchema = list[OutAuthorSchema]
