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
    # container.register(Settings, instance=Settings(), scope=Scope.singleton)
    # settings: Settings = container.resolve(Settings)

    # Настройка базы данных
    DATABASE_URL = "sqlite+aiosqlite:///database.db"
    database_manager = DatabaseManager(DATABASE_URL)
    container.register(
        DatabaseManager, instance=database_manager, scope=Scope.singleton
    )
    # engine = create_async_engine(DATABASE_URL, echo=True)
    # SessionLocal = sessionmaker(
    #     bind=engine,
    #     class_=AsyncSession,
    #     expire_on_commit=False
    # )

    # async def init_models():
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.create_all)

    # initial services
    def init_author_service() -> AuthorService:
        return AuthorService(session_factory=database_manager.SessionLocal)

    # register services
    container.register(BaseAuthorService, factory=init_author_service)

    # register use cases
    container.register(CreateAuthorUseCase)

    return container
