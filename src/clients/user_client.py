from src.clients.http_base import HttpBase

class UserClient:
    def __init__(self, http: HttpBase):
        self.http = http

    def me(self):
        return self.http.get("/user/me")
