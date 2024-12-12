from functools import lru_cache

from punq import Container, Scope

from infra.database.manager import DatabaseManager
from infra.repositories.authors.base import BaseAuthorRepository
from infra.repositories.authors.sqlalchemy_author_repository import SQLAlchemyAuthorRepository
from infra.repositories.books.base import BaseBookRepository
from infra.repositories.books.sqlalchemy_book_repository import SQLAlchemyBookRepository
from logic.services.authors import AuthorNameValidatorService, AuthorService, BaseAuthorService, BaseAuthorValidatorService, ComposedAuthorValidatorService

from logic.services.books import BaseBookService, BaseBookValidatorService, BookService, BookTitleValidatorService, ComposedBookValidatorService
from logic.use_cases.authors.create import CreateAuthorUseCase
from logic.use_cases.authors.delete import DeleteAuthorUseCase
from logic.use_cases.authors.get import GetAuthorUseCase, GetAuthorsUseCase
from logic.use_cases.authors.update import UpdateAuthorUseCase
from logic.use_cases.books.create import CreateBookUseCase
from logic.use_cases.books.delete import DeleteBookUseCase
from logic.use_cases.books.get import GetBookUseCase, GetBooksUseCase
from logic.use_cases.books.update import UpdateBookUseCase
from settings.config import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)


    database_manager = DatabaseManager(settings.db_url)
    container.register(
        DatabaseManager, instance=database_manager, scope=Scope.singleton
    )

    ### authors

    # validators
    container.register(AuthorNameValidatorService)

    def build_author_validators() -> BaseAuthorValidatorService:
        return ComposedAuthorValidatorService(
            validators=[
                container.resolve(AuthorNameValidatorService),
            ]
        )
    
    def build_author_repository() -> BaseAuthorRepository:
        return SQLAlchemyAuthorRepository(
        )
    
    
    container.register(BaseAuthorValidatorService, factory=build_author_validators)
    container.register(BaseAuthorRepository, factory=build_author_repository)

    # initial services
    def init_author_service() -> AuthorService:
        return AuthorService(session_factory=database_manager.SessionLocal, author_repository=container.resolve(BaseAuthorRepository))

    # register services
    container.register(BaseAuthorService, factory=init_author_service)

    # register use cases
    container.register(CreateAuthorUseCase)
    container.register(GetAuthorsUseCase)
    container.register(GetAuthorUseCase)
    container.register(UpdateAuthorUseCase)
    container.register(DeleteAuthorUseCase)


    ### books

    # validators
    container.register(BookTitleValidatorService)

    def build_book_validators() -> BaseBookValidatorService:
        return ComposedBookValidatorService(
            validators=[
                container.resolve(BookTitleValidatorService),
            ]
        )
    
    def build_book_repository() -> BaseBookRepository:
        return SQLAlchemyBookRepository(
        )
    
    
    container.register(BaseBookValidatorService, factory=build_book_validators)

    container.register(BaseBookRepository, factory=build_book_repository)

    # initial services
    def init_book_service() -> BookService:
        return BookService(session_factory=database_manager.SessionLocal, book_repository=container.resolve(BaseBookRepository))

    # register services
    container.register(BaseBookService, factory=init_book_service)

    # register use cases
    container.register(CreateBookUseCase)
    container.register(GetBooksUseCase)
    container.register(GetBookUseCase)
    container.register(UpdateBookUseCase)
    container.register(DeleteBookUseCase)

    ### borrows

    return container
