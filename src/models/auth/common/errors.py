from typing import List, Optional

from pydantic import BaseModel


class ErrorItem(BaseModel):
    reason: str
    message: str


class ErrorResponse(BaseModel):
    code: int
    codeText: str
    status: str
    message: str
    errorCode: int
    errors: List[ErrorItem]
