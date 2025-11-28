def test_register_positive(registered_user_phone):
    # 1) Проверяем, что токен установлен
    token = registered_user_phone.http.token
    assert token is not None, "Токен не был установлен после регистрации"

    # 2) Проверяем доступ к защищённой ручке
    resp = registered_user_phone.http.get("/user/me")
    assert resp.status_code == 200, f"/user/me вернул {resp.status_code}, ожидаем 200"

    # 3) Проверяем структуру ответа (минимальная проверка)
    data = resp.json()
    assert "user" in data, "В ответе отсутствует объект user"
