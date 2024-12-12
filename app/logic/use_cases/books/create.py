from dataclasses import dataclass

from domain.entities.library import Book
from logic.services.books import BaseBookService, BaseBookValidatorService
from logic.use_cases.base import BaseUseCase


@dataclass
class CreateBookUseCase(BaseUseCase):
    book_service: BaseBookService
    validator_service: BaseBookValidatorService

    async def execute(self, book: Book) -> Book:
        self.validator_service.validate(book=book)

        saved_book = await self.book_service.create_book(book=book)

        return saved_book
