from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class BookTitleTooLongException(LogicException):
    title: str

    @property
    def message(self):
        return f"Books's title is too long: {self.title}"
    



@dataclass(eq=False)
class BookNotFoundException(LogicException):

    @property
    def message(self):
        return "Book not found"