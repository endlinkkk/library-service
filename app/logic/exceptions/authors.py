from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class AuthorNameTooLongException(LogicException):
    name: str

    @property
    def message(self):
        return f"Author's name is too long: {self.name}"


@dataclass(eq=False)
class AuthorNotFoundException(LogicException):
    @property
    def message(self):
        return "Author not found"
