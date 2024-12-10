from pydantic import BaseModel


class PaginationOut(BaseModel):
    offset: int
    limit: int
    total: int


class PaginationIn(BaseModel):
    offset: int = 0
    limit: int = 20
