from typing import Optional

from pydantic import BaseModel


class RegisterEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    token: str
    refreshToken: str
