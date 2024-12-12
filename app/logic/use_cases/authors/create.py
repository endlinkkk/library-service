from dataclasses import dataclass

from domain.entities.library import Author
from logic.services.authors import BaseAuthorService, BaseAuthorValidatorService
from logic.use_cases.base import BaseUseCase


@dataclass
class CreateAuthorUseCase(BaseUseCase):
    author_service: BaseAuthorService
    validator_service: BaseAuthorValidatorService

    async def execute(self, author: Author) -> Author:
        self.validator_service.validate(author=author)

        saved_author = await self.author_service.create_author(author=author)

        return saved_author
