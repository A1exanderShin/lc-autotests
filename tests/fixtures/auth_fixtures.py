import random
from uuid import uuid4

import pytest
from src.clients.auth_client import AuthClient

BASE_URL = "https://test2.lototeam.com/api/lotoclub_api/v1"

TEST_EMAIL = "aaa@aaa.aaa"
TEST_EMAIL_PASSWORD = "123123123"

TEST_PHONE = "77000000000"
TEST_PHONE_PASSWORD = "11111111"

TEST_REGISTER_PASSWORD = "123123123"

TEST_IP = "127.0.0.1:3000"
TEST_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
TEST_PLATFORM = "web"


@pytest.fixture
def auth_client():
    return AuthClient(BASE_URL)


@pytest.fixture
def session_id_email(auth_client):
    response = auth_client.check_email(
        email=TEST_EMAIL,
        ip=TEST_IP,
        user_agent=TEST_USER_AGENT
    )

    assert response.status_code == 200, f"check_email failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_email"

    return session_id

@pytest.fixture
def auth_user_email(auth_client, session_id_email):
    response = auth_client.login_email(
        password=TEST_EMAIL_PASSWORD,
        sessionId=session_id_email
    )

    assert response.status_code == 200, f"login failed: {response.text}"

    data = response.json()

    assert "token" in data, "В ответе нет токена"

    return auth_client


@pytest.fixture
def session_id_phone(auth_client):
    response = auth_client.check_phone(
        phone=TEST_PHONE,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT
    )

    assert response.status_code == 200, f"check_phone failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_phone"

    return session_id


@pytest.fixture
def auth_user_phone(auth_client, session_id_phone):
    response = auth_client.login_phone(
        password=TEST_PHONE_PASSWORD,
        sessionId=session_id_phone
    )

    assert response.status_code == 200, f"login failed: {response.text}"

    data = response.json()

    assert "token" in data, "В ответе нет токена"

    return auth_client


@pytest.fixture
def random_email():
    email = f"user_{uuid4().hex[:10]}@pytest.py"
    return email


@pytest.fixture
def random_phone():
    random_integer = random.randint(100000000, 999999999)
    phone = f"77{random_integer}"
    return phone


@pytest.fixture
def session_id_email_new(auth_client, random_email):
    response = auth_client.check_email(
        email=random_email,
        ip=TEST_IP,
        user_agent=TEST_USER_AGENT
    )

    assert response.status_code == 200, f"check_email failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_email"

    return session_id


@pytest.fixture
def session_id_phone_new(auth_client, random_phone):
    response = auth_client.check_phone(
        phone=random_phone,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT
    )

    assert response.status_code == 200, f"check_phone failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_phone"

    return session_id


@pytest.fixture
def registered_user_email(auth_client, session_id_email_new):
    response = auth_client.register_email(
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias="en",
        sessionId=session_id_email_new
    )

    assert response.status_code == 200, f"registration failed: {response.text}"

    data = response.json()

    assert "token" in data, "В ответе нет токена"
    assert "refreshToken" in data, "В ответе нет рефреш-токена"

    if response.status_code == 200:
        token = data.get("token")
        if token:
            auth_client.http.token = token

    return auth_client


@pytest.fixture
def registered_user_phone(auth_client, session_id_phone_new):
    response = auth_client.register_phone(
        password=TEST_REGISTER_PASSWORD,
        sessionId=session_id_phone_new
    )

    assert response.status_code == 200, f"registration failed: {response.text}"

    data = response.json()

    assert "token" in data, "В ответе нет токена"
    assert "refreshToken" in data, "В ответе нет рефреш-токена"


    if response.status_code == 200:
        token = data.get("token")
        if token:
            auth_client.http.token = token

    return auth_client


