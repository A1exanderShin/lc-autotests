from pydantic import BaseModel


class FastRegConfirmResponse(BaseModel):
    code: int
    codeText: str
    gambler_id: int
    token: str
    refresh_token: str
