from dataclasses import dataclass
from domain.entities.library import Author
from logic.services.authors import BaseAuthorService
from logic.use_cases.base import BaseUseCase


@dataclass
class UpdateAuthorUseCase(BaseUseCase):
    author_service: BaseAuthorService

    async def execute(self, author_id: int, author: Author) -> Author:
        author = await self.author_service.update_author(
            author_id=author_id, author=author
        )

        return author
