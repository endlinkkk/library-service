from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from application.api.books.schemas import InBookSchema, OutBookSchema
from application.api.borrows.schemas import InBorrowSchema, OutBorrowSchema
from application.api.filters import PaginationIn, PaginationOut
from application.api.schemas import ApiResponse, ErrorSchema, ListPaginatedResponse
from domain.exceptions.base import ApplicationException

from punq import Container

from logic.init import init_container
from logic.use_cases.borrows.create import CreateBorrowUseCase


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
