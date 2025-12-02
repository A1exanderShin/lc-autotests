import pytest


# ПУСТЫЕ ЗНАЧЕНИЯ
@pytest.mark.parametrize("password, sessionId, description", [
    ("", "valid", "пустой password"),
    ("valid", "", "пустой sessionId"),
    ("", "", "оба поля пустые"),
])
def test_login_phone_empty_values(auth_client, session_id_phone, password, sessionId, description):
    if sessionId == "valid":
        sessionId = session_id_phone

    resp = auth_client.login_phone(
        password=password,
        sessionId=sessionId
    )

    assert resp.status_code in (400, 401), f"{description}: получили {resp.status_code}"


# ОТСУТСТВУЮЩИЕ ПОЛЯ
@pytest.mark.parametrize("payload, description", [
    ({"sessionId": "AAA"}, "нет password"),
    ({"password": "123123123"}, "нет sessionId"),
    ({}, "пустой JSON"),
])
def test_login_phone_missing_fields(auth_client, session_id_phone, payload, description):
    resp = auth_client.http.post("/auth/phone_login", json=payload)

    # В оригинале у тебя один тест ожидает 404 — оставляем как есть
    expected = (400, 401, 404)

    assert resp.status_code in expected, f"{description}: получили {resp.status_code}"


# НЕВЕРНЫЕ ТИПЫ / ФОРМАТ PASSWORD
@pytest.mark.parametrize("password, description", [
    (True, "password = boolean"),
    (123, "password = int"),
    (None, "password = null"),
    (["123"], "password = список"),
    ({"p": "123"}, "password = объект"),
    ("😀😀😀", "password содержит emoji"),
    ("1" * 5000, "слишком длинный password"),
])
def test_login_phone_invalid_password(auth_client, session_id_phone, password, description):
    resp = auth_client.login_phone(
        password=password,
        sessionId=session_id_phone
    )

    assert resp.status_code in (400, 401), f"{description}: получили {resp.status_code}"


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
def test_login_phone_invalid_sessionId(auth_client, session_id_phone, sessionId, description):
    resp = auth_client.login_phone(
        password="123123123",
        sessionId=sessionId
    )

    assert resp.status_code in (400, 401), f"{description}: получили {resp.status_code}"
