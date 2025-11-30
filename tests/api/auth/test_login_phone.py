def test_login_positive(auth_user_phone):
    token = auth_user_phone.http.token
    assert token is not None, "Токен не был установлен после login"

    resp = auth_user_phone.http.get("/user/me")
    assert resp.status_code == 200, f"/user/me вернул {resp.status_code}, ожидаем 200"


def test_login_invalid_password(auth_client, session_id_phone):
    resp = auth_client.login_phone(
        password="WRONG_PASSWORD_123",
        sessionId=session_id_phone
    )

    assert resp.status_code in (400, 401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_invalid_session_id(auth_client):
    resp = auth_client.login_phone(
        password="123123123",
        sessionId="00000000-0000-0000-0000-000000000000"
    )

    assert resp.status_code in (400, 401, 403), (
        f"API неправильно обрабатывает неверный sessionId: {resp.status_code}"
    )
