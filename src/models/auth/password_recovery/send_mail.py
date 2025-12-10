from pydantic import BaseModel


class SendMailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    sessionId: str
