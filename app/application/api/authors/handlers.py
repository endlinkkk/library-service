from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.authors.schemas import AuthorSchema, CreateAuthorSchema
from application.api.filters import PaginationIn, PaginationOut
from application.api.schemas import ApiResponse, ErrorSchema, ListPaginatedResponse
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container
from logic.use_cases.authors.create import CreateAuthorUseCase
from logic.use_cases.authors.get import GetAuthorsUseCase


router = APIRouter(
    tags=["Author"],
)


@router.post(
    "/",
    response_model=ApiResponse[AuthorSchema],
    status_code=status.HTTP_201_CREATED,
    description="Create new author",
    responses={
        status.HTTP_201_CREATED: {"model": AuthorSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_author_handler(
    schema: CreateAuthorSchema, container: Container = Depends(init_container)
) -> ApiResponse[AuthorSchema]:
    """Create new author"""
    use_case: CreateAuthorUseCase = container.resolve(CreateAuthorUseCase)

    try:
        author = await use_case.execute(author=schema.to_entity())
    except ApplicationException as err:
        raise HTTPException(status_code=400, message=err.message)

    return ApiResponse(data=AuthorSchema.from_entity(author))


@router.get(
    "/",
    response_model=ApiResponse[ListPaginatedResponse[AuthorSchema]],
    status_code=status.HTTP_200_OK,
    description="Get authors",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[AuthorSchema]]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_authors_handler(
    pagination_in: PaginationIn = Depends(), container: Container = Depends(init_container)
) -> ApiResponse[ListPaginatedResponse[AuthorSchema]]:
    """Get authors list"""
    use_case: GetAuthorsUseCase = container.resolve(GetAuthorsUseCase)

    try:
        author_list = await use_case.execute(
            pagination=pagination_in
        )
        items = [AuthorSchema.from_entity(obj) for obj in author_list]
        pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )

    except ApplicationException as err:
        raise HTTPException(status_code=400, message=err.message)

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
