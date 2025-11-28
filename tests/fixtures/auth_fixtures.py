import pytest
from src.clients.auth_client import AuthClient

BASE_URL = "https://test2.lototeam.com/api/lotoclub_api/v1"

TEST_EMAIL = "aaa@aaa.aaa"
TEST_EMAIL_PASSWORD = "123123123"

TEST_PHONE = "77000000000"
TEST_PHONE_PASSWORD = "11111111"

TEST_IP = "127.0.0.1:3000"
TEST_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
TEST_PLATFORM = "web"


@pytest.fixture
def auth_client():
    """
    Базовая фикстура для получения AuthClient.
    Другие фикстуры будут использовать её для login / register.
    """
    return AuthClient(BASE_URL)


@pytest.fixture
def session_id_email(auth_client):
    """
    Выполняет check_email → возвращает sessionId.
    Это обязательный шаг как для register, так и для login.
    """
    response = auth_client.check_email(
        email=TEST_EMAIL,
        ip=TEST_IP,
        user_agent=TEST_USER_AGENT
    )

    # Проверяем, что запрос прошёл успешно
    assert response.status_code == 200, f"check_email failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_email"

    return session_id


@pytest.fixture
def auth_user_email(auth_client, session_id_email):
    """
    Авторизация существующего пользователя.
    Возвращает AuthClient, внутри которого уже лежит token.
    """

    response = auth_client.login_email(
        password=TEST_EMAIL_PASSWORD,
        sessionId=session_id_email
    )

    assert response.status_code == 200, f"login failed: {response.text}"

    data = response.json()

    # Проверяем, что токен пришёл
    assert "token" in data, "В ответе нет токена"

    # auth_client.http.token уже установлен внутри login()
    return auth_client


@pytest.fixture
def session_id_phone(auth_client):
    """
    Выполняет check_phone → возвращает sessionId.
    Это обязательный шаг как для register, так и для login.
    """

    response = auth_client.check_phone(
        phone=TEST_PHONE,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT
    )

    # Проверяем, что запрос прошёл успешно
    assert response.status_code == 200, f"check_phone failed: {response.text}"

    data = response.json()
    session_id = data.get("sessionId")

    assert session_id, "sessionId отсутствует в ответе check_phone"

    return session_id

@pytest.fixture
def auth_user_phone(auth_client, session_id_phone):
    """
    Авторизация существующего пользователя.
    Возвращает AuthClient, внутри которого уже лежит token.
    """

    response = auth_client.login_phone(
        password=TEST_PHONE_PASSWORD,
        sessionId=session_id_phone
    )

    assert response.status_code == 200, f"login failed: {response.text}"

    data = response.json()

    # Проверяем, что токен пришёл
    assert "token" in data, "В ответе нет токена"

    # auth_client.http.token уже установлен внутри login()
    return auth_client


