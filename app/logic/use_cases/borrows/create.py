from dataclasses import dataclass

from domain.entities.library import Borrow
from logic.services.books import BaseBookService
from logic.services.borrows import BaseBorrowService, BaseBorrowValidatorService
from logic.use_cases.base import BaseUseCase


@dataclass
class CreateBorrowUseCase(BaseUseCase):
    borrow_service: BaseBorrowService
    book_service: BaseBookService
    validator_service: BaseBorrowValidatorService

    async def execute(self, borrow: Borrow) -> Borrow:
        self.validator_service.validate(borrow=borrow)

        await self.book_service.reduce_the_quantity_by_one(book_id=borrow.book_id)
        saved_borrow = await self.borrow_service.create_borrow(borrow=borrow)

        return saved_borrow
