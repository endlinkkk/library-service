from dataclasses import dataclass
from typing import Iterable

from application.api.filters import PaginationIn
from domain.entities.library import Book
from logic.services.books import BaseBookService
from logic.use_cases.base import BaseUseCase


@dataclass
class GetBooksUseCase(BaseUseCase):
    book_service: BaseBookService

    async def execute(self, pagination: PaginationIn) -> Iterable[Book]:

        books = await self.book_service.get_book_list(pagination=pagination)

        return books
    

@dataclass
class GetBookUseCase(BaseUseCase):
    book_service: BaseBookService

    async def execute(self, book_id: int) -> Book:

        book = await self.book_service.get_book(book_id=book_id)

        return book