from tests.fixtures.auth_fixtures import auth_user_email


def test_login_positive(auth_user_email):
    """
    Позитивный тест авторизации.
    Проверяем:
    - токен установлен
    - токен в правильном заголовке
    - доступ к защищённому эндпоинту работает
    """

    # 1) Проверяем токен
    token = auth_user_email.http.token
    assert token is not None, "Токен не был установлен после login"

    # 2) Делаем запрос к защищённой ручке
    resp = auth_user_email.http.get("/user/me")
    assert resp.status_code == 200, f"/user/me вернул {resp.status_code}, ожидаем 200"


def test_login_invalid_password(auth_client, session_id_email):
    """
    Негатив: логин с неверным паролем.
    Проверяем, что API корректно валидирует пароль.
    """
    resp = auth_client.login_email(
        password="WRONG_PASSWORD_123",
        sessionId=session_id_email
    )

    # В вашем API чаще всего -> 400 или 401
    assert resp.status_code in (400, 401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_invalid_session_id(auth_client):
    """
    Негатив: логин с неверным sessionId.
    """
    resp = auth_client.login_email(
        password="123123123",
        sessionId="00000000-0000-0000-0000-000000000000"
    )

    assert resp.status_code in (400, 401, 403), (
        f"API неправильно обрабатывает неверный sessionId: {resp.status_code}"
    )
