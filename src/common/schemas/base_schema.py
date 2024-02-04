"""Common base schema for all schemas."""
from typing import Optional
from pydantic import BaseModel, field_validator
from src.common.constants.common import PageOrder


class PageBase(BaseModel):
    order: Optional[PageOrder]
    page_no: Optional[int] = 1
    page_size: Optional[int] = 25
    sort: Optional[str]

    class Config:
        use_enum_values = True

    @field_validator("page_no")
    def validate_pageNo(cls, v):
        if v < 1:
            raise ValueError("page_no must be greater than 0")
        return v

    @field_validator("page_size")
    def validate_pageSize(cls, v):
        if v < 1:
            raise ValueError("page_size must be greater than 0")
        return v
