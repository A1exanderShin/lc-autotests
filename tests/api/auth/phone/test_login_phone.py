def test_login_positive(auth_user_phone, assert_response):
    token = auth_user_phone.http.token
    assert token is not None, "Токен не был установлен после login"

    resp = auth_user_phone.http.get("/user/me")

    assert_response(
        resp, expected=(200,), msg=f"Ожидали 200, получили {resp.status_code}"
    )
