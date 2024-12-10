from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.library import Author


@dataclass
class BaseAuthorRepository(ABC):
    @abstractmethod
    def add(self, author: Author) -> Author: ...

    # @abstractmethod
    # def get_by_id(self, author_id: int) -> Author | None:
    #     ...

    # @abstractmethod
    # def get_all(self) -> list[Author]:
    #     ...

    # @abstractmethod
    # def update(self, author: Author) -> Author:
    #     ...

    # @abstractmethod
    # def delete(self, author_id: int) -> None:
    #     ...
