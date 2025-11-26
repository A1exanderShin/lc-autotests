from src.clients.http_base import HttpBase


class AuthClient:
    def __init__(self, base_url: str):
        self.http = HttpBase(base_url)

    def check_email(self, email: str, ip: str, user_agent: str):
        """Шаг 1: проверка email и получение sessionId."""
        payload = {
            "email": email,
            "ip": ip,
            "user_agent": user_agent
        }
        response = self.http.post("/auth/check_email", json=payload)
        return response

    def register(self, password: str, currency_id: int, langAlias: str, sessionId: str):
        """Шаг 2: регистрация по почте."""
        payload = {
            "password": password,
            "currency_id": currency_id,
            "langAlias": langAlias,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/email_register", json=payload)
        return response

    def login(self, password: str, sessionId: str):
        """Шаг 3: логин по почте."""
        payload = {
            "password": password,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/email_login", json=payload)

        # сохраняем токен в http клиент, чтобы другие клиенты могли его использовать
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                self.http.token = token

        return response
