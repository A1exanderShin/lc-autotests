from src.clients.http_base import HttpBase

class AuthClient:
    def __init__(self, base_url: str):
        self.http = HttpBase(base_url)

    # РЕГИСТРАЦИЯ / ВХОД ПО ПОЧТЕ
    def check_email(self, email: str, ip: str, user_agent: str):
        payload = {
            "email": email,
            "ip": ip,
            "user_agent": user_agent
        }
        response = self.http.post("/auth/check_email", json=payload)

        return response

    def register_email(self, password: str, currency_id: int, langAlias: str, sessionId: str):
        payload = {
            "password": password,
            "currency_id": currency_id,
            "langAlias": langAlias,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/email_register", json=payload)

        return response

    def login_email(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/email_login", json=payload)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                self.http.token = token

        return response



    # РЕГИСТРАЦИЯ / ВХОД ПО ТЕЛЕФОНУ
    def check_phone(self, phone: str, ip: str, platform: str, user_agent: str):
        payload = {
            "phone": phone,
            "ip": ip,
            "platform": platform,
            "user_agent": user_agent
        }

        response = self.http.post("/auth/check_phone", json=payload)

        return response

    def register_phone(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId
        }

        response = self.http.post("/auth/register", json=payload)

        return response

    def login_phone(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/login", json=payload)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                self.http.token = token

        return response


