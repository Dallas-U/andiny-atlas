from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    """Pagination details returned with collection responses."""

    page: int
    page_size: int
    total_records: int
    total_pages: int
    returned_records: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated API response."""

    metadata: PaginationMetadata
    items: list[T]
