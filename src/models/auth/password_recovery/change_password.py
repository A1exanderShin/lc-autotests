from pydantic import BaseModel


class ChangePasswordResponse(BaseModel):
    code: int
    codeText: str
    status: str