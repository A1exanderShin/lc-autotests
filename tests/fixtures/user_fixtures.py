import pytest

from src.clients.user_client import UserClient


@pytest.fixture
def user_client_email(auth_user_email):
    return UserClient(auth_user_email.http)


@pytest.fixture
def user_client_phone(auth_user_phone):
    return UserClient(auth_user_phone.http)


@pytest.fixture
def user_client_email_new(registered_user_email):
    return UserClient(registered_user_email.http)


@pytest.fixture
def user_client_phone_new(registered_user_phone):
    return UserClient(registered_user_phone.http)
