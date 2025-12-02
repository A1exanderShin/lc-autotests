from pydantic import BaseModel
from typing import Optional, List


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