from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.library import Author


@dataclass
class BaseAuthorRepository(ABC):
    @abstractmethod
    async def add(self, author: Author) -> Author: ...

    @abstractmethod
    async def get_by_id(self, author_id: int) -> Author | None:
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[Author]:
        ...

    @abstractmethod
    async def update(self, author: Author) -> Author:
        ...

    @abstractmethod
    async def delete(self, author_id: int) -> bool:
        ...
