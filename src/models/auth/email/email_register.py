from pydantic import BaseModel
from typing import Optional

class EmailRegisterResponse(BaseModel):
    code: int
    codeText: str
    status: str
    token: str
    refreshToken: str

def register_email(self, password: str, currency_id: int, langAlias: str, sessionId: str):
    payload = {
        "password": password,
        "currency_id": currency_id,
        "langAlias": langAlias,
        "sessionId": sessionId
    }
    response = self.http.post("/auth/email_register", json=payload)

    parsed = self._parse(response, EmailRegisterResponse)

    if isinstance(parsed, EmailRegisterResponse):
        self.http.token = parsed.token

    return parsed
