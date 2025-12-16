from pydantic import BaseModel


class ConfirmMailCodeResponse(BaseModel):
    code: int
    codeText: str
    status: str