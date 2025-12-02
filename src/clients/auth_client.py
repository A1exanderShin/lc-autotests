from pydantic import ValidationError

from src.clients.http_base import HttpBase
from src.models.auth.common.errors import ErrorResponse
from src.models.auth.email.check_email import CheckEmailResponse
from src.models.auth.email.email_login import LoginEmailResponse
from src.models.auth.email.email_register import EmailRegisterResponse


class AuthClient:
    def __init__(self, base_url: str):
        self.http = HttpBase(base_url)

    def _parse(self, response, model_cls):
        if response.status_code == 200:
            try:
                return model_cls(**response.json())
            except ValidationError:
                return response

        try:
            return ErrorResponse(**response.json())
        except Exception:
            return response

    # РЕГИСТРАЦИЯ / ВХОД ПО ПОЧТЕ
    def check_email(self, email: str, ip: str, user_agent: str):
        payload = {
            "email": email,
            "ip": ip,
            "user_agent": user_agent,
        }

        response = self.http.post("/auth/check_email", json=payload)
        parsed = self._parse(response, CheckEmailResponse)

        return parsed

    def register_email(self, password: str, currency_id: int, langAlias: str, sessionId: str):
        payload = {
            "password": password,
            "currency_id": currency_id,
            "langAlias": langAlias,
            "sessionId": sessionId,
        }

        response = self.http.post("/auth/email_register", json=payload)
        parsed = self._parse(response, EmailRegisterResponse)

        # Если успешный ответ — сохраняем токен
        if isinstance(parsed, EmailRegisterResponse):
            self.http.token = parsed.token

        return parsed

    def login_email(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId,
        }

        response = self.http.post("/auth/email_login", json=payload)
        parsed = self._parse(response, LoginEmailResponse)

        # Если успешный ответ — устанавливаем токен в HttpBase
        if isinstance(parsed, LoginEmailResponse):
            self.http.token = parsed.token

        return parsed



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


