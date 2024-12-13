from dataclasses import dataclass
from domain.entities.library import Book
from logic.services.books import BaseBookService
from logic.use_cases.base import BaseUseCase


@dataclass
class UpdateBookUseCase(BaseUseCase):
    book_service: BaseBookService

    async def execute(self, book_id: int, book: Book) -> Book:
        book = await self.book_service.update_book(book_id=book_id, book=book)

        return book
