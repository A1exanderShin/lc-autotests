from pydantic import BaseModel

class LoginPhoneResponse(BaseModel):
    code: int
    token: str
    refreshToken: str
