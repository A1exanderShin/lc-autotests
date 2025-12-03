from pydantic import BaseModel
from typing import Optional

class RegisterPhoneResponse(BaseModel):
    code: int
    token: str
    refreshToken: str
