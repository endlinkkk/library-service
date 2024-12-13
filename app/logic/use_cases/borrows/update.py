from dataclasses import dataclass

from domain.entities.library import Borrow
from logic.services.books import BaseBookService
from logic.services.borrows import BaseBorrowService
from logic.use_cases.base import BaseUseCase


@dataclass
class UpdateBorrowUseCase(BaseUseCase):
    borrow_service: BaseBorrowService
    book_service: BaseBookService

    async def execute(self, borrow_id) -> Borrow:
        await self.borrow_service.get_borrow(borrow_id=borrow_id)
        borrow = await self.borrow_service.completion_of_the_issue(borrow_id=borrow_id)
        await self.book_service.increase_the_quantity_by_one(book_id=borrow.book_id)

        return borrow
