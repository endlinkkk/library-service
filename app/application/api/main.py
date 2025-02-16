from contextlib import asynccontextmanager
from fastapi import FastAPI
from punq import Container
from application.api.authors.handlers import router as author_router
from application.api.books.handlers import router as book_router
from application.api.borrows.handlers import router as borrow_router
from infra.database.manager import DatabaseManager
from logic.init import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()
    database_manager: DatabaseManager = container.resolve(DatabaseManager)
    await database_manager.init_models()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Library Service", docs_url="/api/docs", debug=True, lifespan=lifespan
    )

    app.include_router(author_router, prefix="/authors")
    app.include_router(book_router, prefix="/books")
    app.include_router(borrow_router, prefix="/borrows")

    return app
