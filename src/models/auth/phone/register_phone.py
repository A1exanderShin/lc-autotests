from typing import Optional

from pydantic import BaseModel


class RegisterPhoneResponse(BaseModel):
    code: int
    token: str
    refreshToken: str
