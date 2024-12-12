from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.books.schemas import InBookSchema, OutBookSchema
from application.api.filters import PaginationIn, PaginationOut
from application.api.schemas import ApiResponse, ErrorSchema, ListPaginatedResponse
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container

from logic.use_cases.books.create import CreateBookUseCase
from logic.use_cases.books.delete import DeleteBookUseCase
from logic.use_cases.books.get import GetBookUseCase, GetBooksUseCase
from logic.use_cases.books.update import UpdateBookUseCase


router = APIRouter(
    tags=["Book"],
)


@router.post(
    "/",
    response_model=ApiResponse[OutBookSchema],
    status_code=status.HTTP_201_CREATED,
    description="Create new book",
    responses={
        status.HTTP_201_CREATED: {"model": OutBookSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_book_handler(
    schema: InBookSchema, container: Container = Depends(init_container)
) -> ApiResponse[OutBookSchema]:
    """Create new book"""
    use_case: CreateBookUseCase = container.resolve(CreateBookUseCase)

    try:
        book = await use_case.execute(book=schema.to_entity())
    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutBookSchema.from_entity(book))



@router.get(
    "/",
    response_model=ApiResponse[ListPaginatedResponse[OutBookSchema]],
    status_code=status.HTTP_200_OK,
    description="Get books",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[OutBookSchema]]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_books_handler(
    pagination_in: PaginationIn = Depends(), container: Container = Depends(init_container)
) -> ApiResponse[ListPaginatedResponse[OutBookSchema]]:
    """Get books list"""
    use_case: GetBooksUseCase = container.resolve(GetBooksUseCase)

    try:
        book_list = await use_case.execute(
            pagination=pagination_in
        )
        items = [OutBookSchema.from_entity(obj) for obj in book_list]
        pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )



@router.get(
    "/{book_id}/",
    response_model=ApiResponse[OutBookSchema],
    status_code=status.HTTP_200_OK,
    description="Get book detail",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutBookSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_book_detail_handler(
    book_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutBookSchema]:
    """Get book detail"""
    use_case: GetBookUseCase = container.resolve(GetBookUseCase)

    try:
        book = await use_case.execute(
            book_id=book_id
        )
        

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutBookSchema.from_entity(book))



@router.put(
    "/{book_id}/",
    response_model=ApiResponse[OutBookSchema],
    status_code=status.HTTP_200_OK,
    description="Update book",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutBookSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def update_book_handler(
    schema: InBookSchema, book_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutBookSchema]:
    """Update book"""
    use_case: UpdateBookUseCase = container.resolve(UpdateBookUseCase)

    try:
        book = await use_case.execute(
            book_id=book_id, book=schema.to_entity()
        )
        

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutBookSchema.from_entity(book))



@router.delete(
    "/{book_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete book",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def delete_book_handler(
    book_id: int, container: Container = Depends(init_container)
):
    """Delete author"""
    use_case: DeleteBookUseCase = container.resolve(DeleteBookUseCase)

    try:
        await use_case.execute(
            book_id=book_id
        )

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return status.HTTP_204_NO_CONTENT