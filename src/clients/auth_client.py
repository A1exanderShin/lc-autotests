from pydantic import ValidationError

from src.clients.http_base import HttpBase
from src.models.auth.common.errors import ErrorResponse
from src.models.auth.email.check_email import CheckEmailResponse
from src.models.auth.email.login_email import LoginEmailResponse
from src.models.auth.email.register_email import RegisterEmailResponse
from src.models.auth.fast_reg.confirm import FastRegConfirmResponse
from src.models.auth.fast_reg.signUp import FastRegSignUpResponse
from src.models.auth.phone.check_phone import CheckPhoneResponse
from src.models.auth.phone.login_phone import LoginPhoneResponse
from src.models.auth.phone.register_phone import RegisterPhoneResponse


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
        parsed = self._parse(response, RegisterEmailResponse)

        # Если успешный ответ — сохраняем токен
        if isinstance(parsed, RegisterEmailResponse):
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
        parsed = self._parse(response, CheckPhoneResponse)

        return parsed

    def register_phone(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId
        }

        response = self.http.post("/auth/register", json=payload)
        parsed = self._parse(response, RegisterPhoneResponse)

        # Если успешный ответ — сохраняем токен
        if isinstance(parsed, RegisterPhoneResponse):
            self.http.token = parsed.token

        return parsed

    def login_phone(self, password: str, sessionId: str):
        payload = {
            "password": password,
            "sessionId": sessionId
        }
        response = self.http.post("/auth/login", json=payload)
        parsed = self._parse(response, LoginPhoneResponse)

        # Если успешный ответ — устанавливаем токен в HttpBase
        if isinstance(parsed, LoginPhoneResponse):
            self.http.token = parsed.token

        return parsed



    # FASTREG
    def signup_phone(self, phone: str, password: str):
        payload = {
            "phone": phone,
            "password": password
        }
        response = self.http.post("/auth/signUp", json=payload)
        parsed = self._parse(response, FastRegSignUpResponse)

        return parsed

    def confirm_phone(self, session_id: str):
        payload = {"session_id": session_id}
        response = self.http.post("/auth/confirm", json=payload)
        parsed = self._parse(response, FastRegConfirmResponse)

        # Если успешный ответ — устанавливаем токен в HttpBase
        if isinstance(parsed, FastRegConfirmResponse):
            self.http.token = parsed.token

        return parsed




