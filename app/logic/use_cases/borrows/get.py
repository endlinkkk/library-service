from dataclasses import dataclass
from typing import Iterable

from application.api.filters import PaginationIn
from domain.entities.library import Borrow
from logic.services.borrows import BaseBorrowService
from logic.use_cases.base import BaseUseCase


@dataclass
class GetBorrowsUseCase(BaseUseCase):
    borrow_service: BaseBorrowService

    async def execute(self, pagination: PaginationIn) -> Iterable[Borrow]:
        borrows = await self.borrow_service.get_borrow_list(pagination=pagination)

        return borrows


@dataclass
class GetBorrowUseCase(BaseUseCase):
    borrow_service: BaseBorrowService

    async def execute(self, borrow_id: int) -> Borrow:
        borrow = await self.borrow_service.get_borrow(borrow_id=borrow_id)

        return borrow
