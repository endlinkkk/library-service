from dataclasses import dataclass

from logic.services.authors import BaseAuthorService
from logic.use_cases.base import BaseUseCase


@dataclass
class DeleteAuthorUseCase(BaseUseCase):
    author_service: BaseAuthorService

    async def execute(self, author_id: int):

        await self.author_service.delete_author(author_id=author_id)
