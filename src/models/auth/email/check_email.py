from pydantic import BaseModel

class CheckEmailResponse(BaseModel):
    code: int
    codeText: str
    status: str
    state: str
    sessionId: str

def check_email(self, email: str, ip: str, user_agent: str):
    payload = {
        "email": email,
        "ip": ip,
        "user_agent": user_agent
    }
    response = self.http.post("/auth/check_email", json=payload)

    parsed = self._parse(response, CheckEmailResponse)

    if isinstance(parsed, CheckEmailResponse):
        return parsed

    return parsed
