from dataclasses import dataclass
from typing import Iterable

from application.api.filters import PaginationIn
from domain.entities.library import Author
from logic.services.authors import BaseAuthorService
from logic.use_cases.base import BaseUseCase


@dataclass
class GetAuthorsUseCase(BaseUseCase):
    author_service: BaseAuthorService

    async def execute(self, pagination: PaginationIn) -> Iterable[Author]:
        authors = await self.author_service.get_author_list(pagination=pagination)

        return authors


@dataclass
class GetAuthorUseCase(BaseUseCase):
    author_service: BaseAuthorService

    async def execute(self, author_id: int) -> Author:
        author = await self.author_service.get_author(author_id=author_id)

        return author
