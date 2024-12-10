from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.authors.schemas import AuthorSchema, CreateAuthorSchema
from application.api.schemas import ApiResponse, ErrorSchema
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container
from logic.use_cases.authors.create import CreateAuthorUseCase


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
    """Create new chat"""
    use_case: CreateAuthorUseCase = container.resolve(CreateAuthorUseCase)

    try:
        author = await use_case.execute(author=schema.to_entity())
    except ApplicationException as err:
        raise HTTPException(status_code=400, message=err.message)

    return ApiResponse(data=AuthorSchema.from_entity(author))


# @router.get(
#     "/",
#     response_model=ApiResponse[ListPaginatedResponse[AuthorSchema]],
#     status_code=status.HTTP_201_CREATED,
#     description="Get authors",
#     responses={
#         status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[AuthorSchema]]},
#         status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
#     },
# )
# async def create_author_handler(
#     schema: CreateAuthorRequestSchema, filters: Query[AuthorFilters], pagination_in: Query[PaginationIn], container: Container = Depends(init_container)
# ) -> CreateChatResponseSchema:
#     """Create new chat"""
#     use_case: CreateAuthorUseCase = container.resolve(CreateAuthorUseCase)

#     try:
#         author_list = await use_case.execute(filters=filters)
#         items = [AuthorSchema.from_entity(obj) for obj in author_list]
#         pagination_out = PaginationOut(
#         offset=pagination_in.offset,
#         limit=pagination_in.limit,
#         total=len(items),
#     )

#     except ServiceException as err:
#         raise HttpException(status_code=400, message=err.message)

#     return ApiResponse(
#         data=ListPaginatedResponse(items=items, pagination=pagination_out)
#     )
