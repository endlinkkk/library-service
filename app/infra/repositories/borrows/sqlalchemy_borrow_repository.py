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


# class BorrowModel(Base):
#     __tablename__ = "borrows"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
#     reader_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
#     return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime, default=datetime.now, onupdate=datetime.now
#     )

#     book: Mapped["BookModel"] = relationship("BookModel", back_populates="borrows")

# async def get_by_id(self, book_id: int, session: Session) -> BookEntity | None:
#     result = await session.execute(select(BookModel).where(BookModel.id == book_id))
#     book_model = result.scalars().one_or_none()
#     if book_model:
#         return BookEntity(
#             id=book_model.id,
#             title=book_model.title,
#             description=book_model.description,
#             author_id=book_model.author_id,
#             available_copies=book_model.available_copies,
#             created_at=book_model.created_at,
#             updated_at=book_model.updated_at,
#         )

# async def get_all(
#     self, session: Session, limit: int = 20, offset: int = 0
# ) -> list[BookEntity]:
#     result = await session.execute(select(BookModel).offset(offset).limit(limit))
#     book_models = result.scalars().all()
#     return [
#         BookEntity(
#             id=book_model.id,
#             title=book_model.title,
#             description=book_model.description,
#             author_id=book_model.author_id,
#             available_copies=book_model.available_copies,
#             created_at=book_model.created_at,
#             updated_at=book_model.updated_at,
#         )
#         for book_model in book_models
#     ]

# async def update(
#     self, session: Session, book_id: int, book: BookEntity
# ) -> BookEntity | None:
#     result = await session.execute(select(BookModel).where(BookModel.id == book_id))
#     book_model = result.scalars().one_or_none()

#     if book_model:
#         book_model.title = book.title
#         book_model.description = book.description
#         book_model.available_copies = book.available_copies
#         book_model.author_id = book.author_id
#         session.flush()
#         return BookEntity(
#             id=book_model.id,
#             title=book_model.title,
#             description=book_model.description,
#             author_id=book_model.author_id,
#             available_copies=book_model.available_copies,
#             created_at=book_model.created_at,
#             updated_at=book_model.updated_at,
#         )
#     return None

# async def delete(self, session: Session, book_id: int) -> bool:
#     result = await session.execute(select(BookModel).where(BookModel.id == book_id))
#     book_model = result.scalars().one_or_none()
#     if book_model:
#         await session.delete(book_model)
#         await session.flush()
#         return True
#     return False


# async def reduce_by_one(self, session: Session, book_id: int) -> bool:
#     result = await session.execute(select(BookModel).where(BookModel.id == book_id))
#     book_model: BookModel = result.scalars().one_or_none()
#     if book_model and book_model.available_copies >= 1:
#         book_model.available_copies -= 1
#         await session.flush()
#         return True
#     return False
