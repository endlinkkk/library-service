from dataclasses import dataclass
from logic.services.books import BaseBookService
from logic.use_cases.base import BaseUseCase


@dataclass
class DeleteBookUseCase(BaseUseCase):
    book_service: BaseBookService

    async def execute(self, book_id: int):
        await self.book_service.delete_book(book_id=book_id)
