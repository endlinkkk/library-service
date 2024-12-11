from functools import lru_cache

from punq import Container, Scope

from infra.database.manager import DatabaseManager
from logic.services.authors import AuthorService, BaseAuthorService

from logic.use_cases.authors.create import CreateAuthorUseCase
from settings.config import Settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from infra.database.models import Base


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)

    # Настройка базы данных
    # DATABASE_URL = "sqlite+aiosqlite:///database.db"
    # DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
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

    return container
