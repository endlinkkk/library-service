from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.borrows.schemas import InBorrowSchema, OutBorrowSchema
from application.api.filters import PaginationIn, PaginationOut
from application.api.schemas import ApiResponse, ErrorSchema, ListPaginatedResponse
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container
from logic.use_cases.borrows.create import CreateBorrowUseCase
from logic.use_cases.borrows.get import GetBorrowUseCase, GetBorrowsUseCase
from logic.use_cases.borrows.update import UpdateBorrowUseCase


router = APIRouter(
    tags=["Borrow"],
)


@router.post(
    "/",
    response_model=ApiResponse[OutBorrowSchema],
    status_code=status.HTTP_201_CREATED,
    description="Create new borrow",
    responses={
        status.HTTP_201_CREATED: {"model": OutBorrowSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_borrow_handler(
    schema: InBorrowSchema, container: Container = Depends(init_container)
) -> ApiResponse[OutBorrowSchema]:
    """Create new borrow"""
    use_case: CreateBorrowUseCase = container.resolve(CreateBorrowUseCase)

    try:
        borrow = await use_case.execute(borrow=schema.to_entity())
    except ApplicationException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err.message},
        )

    return ApiResponse(data=OutBorrowSchema.from_entity(borrow))


@router.get(
    "/",
    response_model=ApiResponse[ListPaginatedResponse[OutBorrowSchema]],
    status_code=status.HTTP_200_OK,
    description="Get borrows",
    responses={
        status.HTTP_200_OK: {
            "model": ApiResponse[ListPaginatedResponse[OutBorrowSchema]]
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_borrows_handler(
    pagination_in: PaginationIn = Depends(),
    container: Container = Depends(init_container),
) -> ApiResponse[ListPaginatedResponse[OutBorrowSchema]]:
    """Get borrows list"""
    use_case: GetBorrowsUseCase = container.resolve(GetBorrowsUseCase)

    try:
        borrow_list = await use_case.execute(pagination=pagination_in)
        items = [OutBorrowSchema.from_entity(obj) for obj in borrow_list]
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
    "/{borrow_id}/",
    response_model=ApiResponse[OutBorrowSchema],
    status_code=status.HTTP_200_OK,
    description="Get borrow detail",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutBorrowSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_borrow_detail_handler(
    borrow_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutBorrowSchema]:
    """Get borrow detail"""
    use_case: GetBorrowUseCase = container.resolve(GetBorrowUseCase)

    try:
        borrow = await use_case.execute(borrow_id=borrow_id)

    except ApplicationException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err.message},
        )

    return ApiResponse(data=OutBorrowSchema.from_entity(borrow))


@router.patch(
    "/{borrow_id}/return",
    response_model=ApiResponse[OutBorrowSchema],
    status_code=status.HTTP_200_OK,
    description="Update book",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[OutBorrowSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def update_borrow_handler(
    borrow_id: int, container: Container = Depends(init_container)
) -> ApiResponse[OutBorrowSchema]:
    """Update borrow"""
    use_case: UpdateBorrowUseCase = container.resolve(UpdateBorrowUseCase)

    try:
        borrow = await use_case.execute(borrow_id=borrow_id)

    except ApplicationException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err.message},
        )

    return ApiResponse(data=OutBorrowSchema.from_entity(borrow))
