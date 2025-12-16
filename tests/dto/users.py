from dataclasses import dataclass

from src.clients.auth_client import AuthClient


@dataclass
class RegisteredEmailUser:
    client: AuthClient
    email: str
