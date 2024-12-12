from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.library import Book


@dataclass
class BaseBookRepository(ABC):
    @abstractmethod
    async def add(self, book: Book) -> Book: ...

    @abstractmethod
    async def get_by_id(self, book_id: int) -> Book | None:
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[Book]:
        ...

    @abstractmethod
    async def update(self, book: Book) -> Book:
        ...

    @abstractmethod
    async def delete(self, book_id: int) -> bool:
        ...
