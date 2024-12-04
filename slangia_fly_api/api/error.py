from enum import Enum
from pydantic import BaseModel


class ErrorKind(str, Enum):
    internal_error: str = "INTERNAL_ERROR"
    not_found: str = "NOT_FOUND"


class ErrorResponse(BaseModel):
    error_kind: ErrorKind
    error: str
