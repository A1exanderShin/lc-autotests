import pytest

# ПУСТЫЕ И ОТСУТСТВУЮЩИЕ ПОЛЯ
@pytest.mark.parametrize("password, sessionId, description", [
    ("", "valid", "пустой password"),
    ("valid", "", "пустой sessionId"),
    ("", "", "оба поля пустые"),
])
def test_login_email_empty_values(auth_client, session_id_email, password, sessionId, description, assert_response):
    if sessionId == "valid":
        sessionId = session_id_email

    resp = auth_client.login_email(
        password=password,
        sessionId=sessionId
    )

    assert_response(resp, expected=(400, 401, 404), msg=description)


@pytest.mark.parametrize("payload, description", [
    ({"sessionId": "AAA"}, "нет password"),
    ({"password": "123123123"}, "нет sessionId"),
    ({}, "пустой JSON"),
])
def test_login_email_missing_fields(auth_client, session_id_email, payload, description, assert_response):
    resp = auth_client.http.post("/auth/email_login", json=payload)

    assert_response(resp, expected=(400, 401, 404), msg=description)


# НЕВЕРНЫЕ ТИПЫ / ФОРМАТ PASSWORD
@pytest.mark.parametrize("password, description", [
    (123123123, "password = null"),
    (True, "password = boolean"),
    (None, "password = null"),
    (["123"], "password = список"),
    ({"p": "123"}, "password = объект"),
    ("😀😀😀123123123", "password содержит emoji"),
    ("1" * 5000, "слишком длинный password"),
])
def test_login_email_invalid_password(auth_client, session_id_email, password, description, assert_response):
    resp = auth_client.login_email(
        password=password,
        sessionId=session_id_email
    )

    assert_response(resp, expected=(400,), msg=description)


# НЕВЕРНЫЕ ТИПЫ / ФОРМАТ sessionId
@pytest.mark.parametrize("sessionId, description", [
    (True, "sessionId = boolean"),
    (123, "sessionId = int"),
    (None, "sessionId = null"),
    (["abc"], "sessionId = список"),
    ({"id": "abc"}, "sessionId = объект"),
    ("😀😀😀", "sessionId = emoji"),
    ("1" * 5000, "слишком длинный sessionId"),
])
def test_login_email_invalid_sessionId(auth_client, session_id_email, sessionId, description, assert_response):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=sessionId
    )

    assert_response(resp, expected=(400,), msg=description)
