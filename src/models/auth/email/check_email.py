from pydantic import BaseModel


class CheckEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    state: str
    sessionId: str
