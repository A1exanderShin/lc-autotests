from pydantic import BaseModel


class LoginEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    token: str
    refreshToken: str
    langAlias: str
