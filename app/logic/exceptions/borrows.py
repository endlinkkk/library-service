from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class BorrowReaderNameTooLongException(LogicException):
    reader_name: str

    @property
    def message(self):
        return f"Borrow reader name is too long: {self.reader_name}"
