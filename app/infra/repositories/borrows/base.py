from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.library import Borrow


@dataclass
class BaseBorrowRepository(ABC):
    @abstractmethod
    async def add(self, borrow: Borrow) -> Borrow: ...

    @abstractmethod
    async def get_by_id(self, borrow_id: int) -> Borrow | None: ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[Borrow]: ...

    @abstractmethod
    async def completion_issue(self, borrow_id: int) -> Borrow: ...
