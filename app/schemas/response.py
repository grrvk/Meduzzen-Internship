from typing import Any, Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar('DataT')


class Response(BaseModel, Generic[DataT]):
    status_code: int
    detail: str
    result: Any





