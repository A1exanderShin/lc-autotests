from pydantic import BaseModel

class FastRegSignUpResponse(BaseModel):
    code: int
    codeText: str
    state: str
    session_id: str
