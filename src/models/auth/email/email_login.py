from pydantic import BaseModel

class LoginEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    token: str
    refreshToken: str
    langAlias: str

def login_email(self, password: str, sessionId: str):
    payload = {
        "password": password,
        "sessionId": sessionId
    }
    response = self.http.post("/auth/email_login", json=payload)

    parsed = self._parse(response, LoginEmailResponse)

    if isinstance(parsed, LoginEmailResponse):
        self.http.token = parsed.token

    return parsed
