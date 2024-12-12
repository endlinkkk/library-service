from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.authors.schemas import OutAuthorSchema, InAuthorSchema
from application.api.filters import PaginationIn, PaginationOut
from application.api.schemas import ApiResponse, ErrorSchema, ListPaginatedResponse
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container
from logic.use_cases.authors.create import CreateAuthorUseCase
from logic.use_cases.authors.delete import DeleteAuthorUseCase
from logic.use_cases.authors.get import GetAuthorUseCase, GetAuthorsUseCase
from logic.use_cases.authors.update import UpdateAuthorUseCase


router = APIRouter(
    tags=["Author"],
)


@router.post(
    "/",
    response_model=ApiResponse[OutAuthorSchema],
    status_code=status.HTTP_201_CREATED,
    description="Create new author",
    responses={
        status.HTTP_201_CREATED: {"model": OutAuthorSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_author_handler(
    schema: InAuthorSchema, container: Container = Depends(init_container)
) -> ApiResponse[OutAuthorSchema]:
    """Create new author"""
    use_case: CreateAuthorUseCase = container.resolve(CreateAuthorUseCase)

    try:
        author = await use_case.execute(author=schema.to_entity())
    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutAuthorSchema.from_entity(author))


@router.get(
    "/",
    response_model=ApiResponse[ListPaginatedResponse[OutAuthorSchema]],
    status_code=status.HTTP_200_OK,
    description="Get authors",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[ListPaginatedResponse[OutAuthorSchema]]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_authors_handler(
    pagination_in: PaginationIn = Depends(), container: Container = Depends(init_container)
) -> ApiResponse[ListPaginatedResponse[OutAuthorSchema]]:
    """Get authors list"""
    use_case: GetAuthorsUseCase = container.resolve(GetAuthorsUseCase)

    try:
        author_list = await use_case.execute(
            pagination=pagination_in
        )
        items = [OutAuthorSchema.from_entity(obj) for obj in author_list]
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
    "/{author_id}/",
    response_model=ApiResponse[OutAuthorSchema],
    status_code=status.HTTP_200_OK,
    description="Get author detail",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutAuthorSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_author_detail_handler(
    author_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutAuthorSchema]:
    """Get author detail"""
    use_case: GetAuthorUseCase = container.resolve(GetAuthorUseCase)

    try:
        author = await use_case.execute(
            author_id=author_id
        )
        

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutAuthorSchema.from_entity(author))



@router.put(
    "/{author_id}/",
    response_model=ApiResponse[OutAuthorSchema],
    status_code=status.HTTP_200_OK,
    description="Update author",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutAuthorSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def update_author_handler(
    schema: InAuthorSchema, author_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutAuthorSchema]:
    """Update book"""
    use_case: UpdateAuthorUseCase = container.resolve(UpdateAuthorUseCase)

    try:
        author = await use_case.execute(
            author_id=author_id, author=schema.to_entity()
        )
        

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return ApiResponse(data=OutAuthorSchema.from_entity(author))



@router.delete(
    "/{author_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete author",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def delete_author_handler(
    author_id: int, container: Container = Depends(init_container)
):
    """Delete author"""
    use_case: DeleteAuthorUseCase = container.resolve(DeleteAuthorUseCase)

    try:
        await use_case.execute(
            author_id=author_id
        )

    except ApplicationException as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": err.message},
            )

    return status.HTTP_204_NO_CONTENT