from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from src.common.constants.common import ApiResult
from src.common.schemas.base_schema import PageBase

DataT = TypeVar("DataT")


class ResponseBase(BaseModel, Generic[DataT]):
    result: str = ApiResult.SUCCESS.value
    msg: str = "API 요청에 성공했습니다."
    msg_detail: Optional[str] = None
    data: Optional[DataT] = None


class ResponsePage(BaseModel, Generic[DataT]):
    total_row: Optional[int] = 0
    list: Optional[DataT] = []
    page: Optional[PageBase] = None
