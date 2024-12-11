from functools import lru_cache

from punq import Container, Scope

from infra.database.manager import DatabaseManager
from logic.services.authors import AuthorService, BaseAuthorService

from logic.use_cases.authors.create import CreateAuthorUseCase
from logic.use_cases.authors.get import GetAuthorsUseCase
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


    # initial services
    def init_author_service() -> AuthorService:
        return AuthorService(session_factory=database_manager.SessionLocal)

    # register services
    container.register(BaseAuthorService, factory=init_author_service)

    # register use cases
    container.register(CreateAuthorUseCase)
    container.register(GetAuthorsUseCase)

    return container
