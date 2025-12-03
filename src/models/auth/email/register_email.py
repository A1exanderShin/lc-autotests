from pydantic import BaseModel
from typing import Optional

class RegisterEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    token: str
    refreshToken: str

