def test_register_positive(registered_user_email):
    token = registered_user_email.http.token
    assert token is not None, "Токен не был установлен после регистрации"

    resp = registered_user_email.http.get("/user/me")
    assert resp.status_code == 200, f"/user/me вернул {resp.status_code}, ожидаем 200"

    data = resp.json()
    assert "user" in data, "В ответе отсутствует объект user"
