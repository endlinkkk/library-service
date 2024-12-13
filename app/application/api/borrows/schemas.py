from datetime import datetime
from pydantic import BaseModel

from domain.entities.library import Borrow as BorrowEntity


class InBorrowSchema(BaseModel):
    book_id: int
    reader_name: str

    def to_entity(self) -> BorrowEntity:
        return BorrowEntity(
            book_id=self.book_id,
            reader_name=self.reader_name,
        )


class OutBorrowSchema(BaseModel):
    id: int
    book_id: int
    reader_name: str
    borrow_date: datetime
    return_date: datetime | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(borrow: BorrowEntity) -> "OutBorrowSchema":
        return OutBorrowSchema(
            id=borrow.id,
            book_id=borrow.book_id,
            reader_name=borrow.reader_name,
            borrow_date=borrow.borrow_date,
            return_date=borrow.return_date,
            created_at=borrow.created_at,
            updated_at=borrow.updated_at,
        )
