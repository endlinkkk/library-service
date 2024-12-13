from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.future import select


from domain.entities.library import Borrow as BorrowEntity

from infra.database.models import BorrowModel
from dataclasses import dataclass

from infra.repositories.borrows.base import BaseBorrowRepository


@dataclass
class SQLAlchemyBorrowRepository(BaseBorrowRepository):
    async def add(self, borrow: BorrowEntity, session: Session) -> BorrowEntity:
        borrow_model = BorrowModel(
            book_id=borrow.book_id,
            reader_name=borrow.reader_name,
            borrow_date=borrow.borrow_date,
        )
        session.add(borrow_model)
        await session.flush()
        return BorrowEntity(
            id=borrow_model.id,
            book_id=borrow_model.book_id,
            reader_name=borrow_model.reader_name,
            borrow_date=borrow_model.borrow_date,
            return_date=borrow_model.return_date,
            created_at=borrow_model.created_at,
            updated_at=borrow_model.updated_at,
        )

    async def get_by_id(self, borrow_id: int, session: Session) -> BorrowEntity | None:
        result = await session.execute(
            select(BorrowModel).where(BorrowModel.id == borrow_id)
        )
        borrow_model = result.scalars().one_or_none()
        if borrow_model:
            return BorrowEntity(
                id=borrow_model.id,
                book_id=borrow_model.book_id,
                reader_name=borrow_model.reader_name,
                borrow_date=borrow_model.borrow_date,
                return_date=borrow_model.return_date,
                created_at=borrow_model.created_at,
                updated_at=borrow_model.updated_at,
            )

    async def get_all(
        self, session: Session, limit: int = 20, offset: int = 0
    ) -> list[BorrowEntity]:
        result = await session.execute(select(BorrowModel).offset(offset).limit(limit))
        borrow_models = result.scalars().all()
        return [
            BorrowEntity(
                id=borrow_model.id,
                book_id=borrow_model.book_id,
                reader_name=borrow_model.reader_name,
                borrow_date=borrow_model.borrow_date,
                return_date=borrow_model.return_date,
                created_at=borrow_model.created_at,
                updated_at=borrow_model.updated_at,
            )
            for borrow_model in borrow_models
        ]

    async def completion_issue(self, session: Session, borrow_id: int) -> BorrowEntity:
        result = await session.execute(
            select(BorrowModel).where(BorrowModel.id == borrow_id)
        )
        borrow_model = result.scalars().one_or_none()
        if borrow_model:
            borrow_model.return_date = datetime.now()
            session.flush()
            return BorrowEntity(
                id=borrow_model.id,
                book_id=borrow_model.book_id,
                reader_name=borrow_model.reader_name,
                borrow_date=borrow_model.borrow_date,
                return_date=borrow_model.return_date,
                created_at=borrow_model.created_at,
                updated_at=borrow_model.updated_at,
            )
