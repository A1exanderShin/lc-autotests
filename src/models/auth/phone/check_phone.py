from pydantic import BaseModel


class CheckPhoneResponse(BaseModel):
    code: int
    codeText: str
    status: str
    state: str
    sessionId: str
