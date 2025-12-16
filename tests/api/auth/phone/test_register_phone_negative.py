import pytest

from tests.fixtures.auth_fixtures import (
    TEST_IP,
    TEST_PLATFORM,
    TEST_REGISTER_PASSWORD,
    TEST_USER_AGENT,
)

# ==========================================================
# 1. ОТСУТСТВУЮЩИЕ ПОЛЯ (STRUCTURE)
# ==========================================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "use_password, use_session, description",
    [
        (False, False, "пустой JSON"),
        (False, True, "нет password"),
        (True, False, "нет sessionId"),
    ],
)
def test_register_phone_missing_fields(
    auth_client,
    session_id_phone_new,  # флоу: check_phone → получить sessionId
    use_password,
    use_session,
    description,
    assert_response,
):

    payload = {}

    if use_password:
        payload["password"] = TEST_REGISTER_PASSWORD

    if use_session:
        payload["sessionId"] = session_id_phone_new

    resp = auth_client.http.post("/auth/register", json=payload)

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Отсутствуют обязательные поля: {description}",
    )


# ==========================================================
# 2. НЕВАЛИДНЫЙ password
# ==========================================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "password, description",
    [
        ("", "пустой password"),
        (" " * 5, "password из пробелов"),
        (True, "password = boolean"),
        (123456, "password = int"),
        (None, "password = null"),
        (["123"], "password = список"),
        ({"p": "123"}, "password = объект"),
        ("1" * 5000, "слишком длинный password"),
    ],
)
def test_register_phone_invalid_password(
    auth_client, session_id_phone_new, password, description, assert_response
):

    resp = auth_client.register_phone(password=password, sessionId=session_id_phone_new)

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Неверное значение password: {description}",
    )


# ==========================================================
# 3. НЕВАЛИДНЫЙ sessionId
# ==========================================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "sessionId, description",
    [
        ("", "пустой sessionId"),
        (" " * 5, "sessionId из пробелов"),
        (123, "sessionId = int"),
        (True, "sessionId = boolean"),
        (None, "sessionId = null"),
        ([], "sessionId = список"),
        ({"id": "123"}, "sessionId = объект"),
        ("😀😀😀", "sessionId = emoji"),
        ("1" * 5000, "слишком длинный sessionId"),
    ],
)
def test_register_phone_invalid_sessionId(
    auth_client, session_id_phone_new, sessionId, description, assert_response
):

    resp = auth_client.register_phone(
        password=TEST_REGISTER_PASSWORD,
        sessionId=sessionId,
    )

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Неверное значение sessionId: {description}",
    )
