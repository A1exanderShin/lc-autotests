import random
from uuid import uuid4

import pytest

from src.clients.auth_client import AuthClient
from src.models.auth.email.check_email import CheckEmailResponse
from src.models.auth.email.login_email import LoginEmailResponse
from src.models.auth.email.register_email import RegisterEmailResponse
from src.models.auth.fast_reg.confirm import FastRegConfirmResponse
from src.models.auth.fast_reg.signUp import FastRegSignUpResponse
from src.models.auth.phone.check_phone import CheckPhoneResponse
from src.models.auth.phone.login_phone import LoginPhoneResponse
from src.models.auth.phone.register_phone import RegisterPhoneResponse
from tests.dto.users import RegisteredEmailUser

# захадкодили урлу, нужно будет сделать конфиг для смены стенда
BASE_URL = "https://test2.lototeam.com/api/lotoclub_api/v1"

TEST_EMAIL = "aaa@aaa.aaa"
TEST_EMAIL_PASSWORD = "123123123"

TEST_PHONE = "77000000000"
TEST_PHONE_PASSWORD = "11111111"

TEST_REGISTER_PASSWORD = "123123123"

TEST_IP = "127.0.0.1:3000"
TEST_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/142.0.0.0 Safari/537.36"
)
TEST_PLATFORM = "web"


@pytest.fixture
def auth_client():
    return AuthClient(BASE_URL)


# ============================================================
# EMAIL FIXTURES
# ============================================================


@pytest.fixture
def session_id_email(auth_client):
    response = auth_client.check_email(
        email=TEST_EMAIL, ip=TEST_IP, user_agent=TEST_USER_AGENT
    )

    assert isinstance(response, CheckEmailResponse), f"check_email failed: {response}"

    return response.sessionId


@pytest.fixture
def auth_user_email(auth_client, session_id_email):
    response = auth_client.login_email(
        password=TEST_EMAIL_PASSWORD, sessionId=session_id_email
    )

    # Теперь response — LoginEmailResponse
    assert isinstance(
        response, LoginEmailResponse
    ), f"login_email returned error: {response}"

    # Токен уже установлен внутри клиента
    assert auth_client.http.token, "Token not set in AuthClient"

    return auth_client


@pytest.fixture
def session_id_email_new(auth_client, random_email):
    response = auth_client.check_email(
        email=random_email, ip=TEST_IP, user_agent=TEST_USER_AGENT
    )

    assert isinstance(response, CheckEmailResponse), f"check_email failed: {response}"

    return response.sessionId


@pytest.fixture
def registered_user_email(auth_client, random_email):
    email = random_email

    check_resp = auth_client.check_email(email, TEST_IP, TEST_USER_AGENT)
    assert isinstance(check_resp, CheckEmailResponse)

    reg_resp = auth_client.register_email(
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias="en",
        sessionId=check_resp.sessionId,
    )
    assert isinstance(reg_resp, RegisterEmailResponse)

    return RegisteredEmailUser(client=auth_client, email=email)


# ============================================================
# PHONE FIXTURES
# ============================================================


@pytest.fixture
def session_id_phone(auth_client):
    response = auth_client.check_phone(
        phone=TEST_PHONE, ip=TEST_IP, platform=TEST_PLATFORM, user_agent=TEST_USER_AGENT
    )

    # Новая проверка: response — это Pydantic модель
    assert isinstance(response, CheckPhoneResponse), f"check_phone failed: {response}"

    return response.sessionId


@pytest.fixture
def auth_user_phone(auth_client, session_id_phone):
    response = auth_client.login_phone(
        password=TEST_PHONE_PASSWORD, sessionId=session_id_phone
    )

    # Теперь response — LoginPhoneResponse
    assert isinstance(
        response, LoginPhoneResponse
    ), f"login_phone returned error: {response}"

    # Токен уже установлен внутри клиента
    assert auth_client.http.token, "Token not set in AuthClient"

    return auth_client


@pytest.fixture
def session_id_phone_new(auth_client, random_phone):
    response = auth_client.check_phone(
        phone=random_phone,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT,
    )

    assert isinstance(response, CheckPhoneResponse), f"check_phone failed: {response}"

    return response.sessionId


@pytest.fixture
def registered_user_phone(auth_client, session_id_phone_new):
    response = auth_client.register_phone(
        password=TEST_REGISTER_PASSWORD, sessionId=session_id_phone_new
    )

    assert isinstance(
        response, RegisterPhoneResponse
    ), f"register_phone returned error: {response}"

    assert auth_client.http.token, "Token not set in AuthClient"

    return auth_client


# ============================================================
# FASTREG FIXTURES
# ============================================================


@pytest.fixture
def fastreg_phone_session_id(auth_client, random_phone):
    response = auth_client.signup_phone(
        phone=random_phone, password=TEST_REGISTER_PASSWORD
    )

    # Новая проверка: response — это Pydantic модель
    assert isinstance(response, FastRegSignUpResponse), f"signUp failed: {response}"

    return response.session_id


@pytest.fixture
def fastreg_phone_user(random_phone):
    client = AuthClient(BASE_URL)

    # signup phone
    signup_resp = client.signup_phone(
        phone=random_phone, password=TEST_REGISTER_PASSWORD
    )
    assert isinstance(signup_resp, FastRegSignUpResponse)

    # confirm phone
    confirm_resp = client.confirm_phone(signup_resp.session_id)
    assert isinstance(confirm_resp, FastRegConfirmResponse)
    assert client.http.token, "Token not set"

    return client


@pytest.fixture
def fastreg_email_session_id(auth_client, random_email):
    response = auth_client.signup_email(
        email=random_email,
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias="en",
    )

    # Новая проверка: response — это Pydantic модель
    assert isinstance(response, FastRegSignUpResponse), f"signUp failed: {response}"

    return response.session_id


@pytest.fixture
def fastreg_email_user(random_email):
    client = AuthClient(BASE_URL)

    signup_resp = client.signup_email(
        email=random_email,
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias="en",
    )
    assert isinstance(signup_resp, FastRegSignUpResponse)

    confirm_resp = client.confirm_email(signup_resp.session_id)
    assert isinstance(confirm_resp, FastRegConfirmResponse)
    assert client.http.token, "Token not set"

    return client


# ============================================================
# PASSWORD RECOVERY
# ============================================================

@pytest.fixture
def password_recovery_email_session(registered_user_email):
    email = registered_user_email.email

    guest = AuthClient(BASE_URL)

    send_resp = guest.send_mail(email)
    assert send_resp.code == 200

    confirm_resp = guest.confirm_mail_code(
        mail_code="111111",
        session_id=send_resp.sessionId
    )
    assert confirm_resp.status == "success"

    return send_resp.sessionId


# ============================================================
# RANDOM DATA
# ============================================================


@pytest.fixture
def random_email():
    return f"user_{uuid4().hex[:10]}@pytest.py"


@pytest.fixture
def random_phone():
    random_integer = random.randint(100000000, 999999999)
    return f"77{random_integer}"
