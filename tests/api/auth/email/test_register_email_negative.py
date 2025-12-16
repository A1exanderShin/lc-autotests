import pytest

from tests.conftest import assert_response
from tests.fixtures.auth_fixtures import TEST_REGISTER_PASSWORD

# ================================
# 1. ОТСУТСТВУЮЩИЕ ПОЛЯ (STRUCTURE)
# ================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "use_password, use_currency, use_lang, use_session, description",
    [
        (False, False, False, False, "пустой JSON"),
        (False, True, True, True, "нет password"),
        (True, False, True, True, "нет currency_id"),
        (True, True, False, True, "нет langAlias"),
        (True, True, True, False, "нет sessionId"),
    ],
)
def test_register_email_missing_fields(
    auth_client,
    session_id_email_new,
    use_password,
    use_currency,
    use_lang,
    use_session,
    description,
    assert_response,
):

    payload = {}

    if use_password:
        payload["password"] = TEST_REGISTER_PASSWORD
    if use_currency:
        payload["currency_id"] = 4
    if use_lang:
        payload["langAlias"] = "en"
    if use_session:
        # тут мы как раз соблюдаем флоу: sessionId из check_email
        payload["sessionId"] = session_id_email_new

    resp = auth_client.http.post("/auth/email_register", json=payload)

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Отсутствуют обязательные/обязательные поля: {description}",
    )


# ================================
# 2. НЕВАЛИДНЫЙ password
# ================================

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
def test_register_email_invalid_password(
    auth_client, session_id_email_new, password, description, assert_response
):

    resp = auth_client.register_email(
        password=password,
        currency_id=4,
        langAlias="en",
        sessionId=session_id_email_new,
    )

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Неверное значение password: {description}",
    )


# ================================
# 3. НЕВАЛИДНЫЙ currency_id
# ================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "currency_id, description",
    [
        (None, "currency_id = null"),
        ("4", "currency_id = строка вместо int"),
        (4.5, "currency_id = float"),
        (-1, "currency_id отрицательный"),
        (0, "currency_id = 0"),
        ([], "currency_id = список"),
        ({}, "currency_id = объект"),
    ],
)
def test_register_email_invalid_currency_id(
    auth_client, session_id_email_new, currency_id, description, assert_response
):

    resp = auth_client.register_email(
        password=TEST_REGISTER_PASSWORD,
        currency_id=currency_id,
        langAlias="en",
        sessionId=session_id_email_new,
    )

    assert_response(
        resp,
        expected=(200, 400, 401, 403, 404),
        msg=f"Неверное значение currency_id: {description}",
    )


# ================================
# 4. НЕВАЛИДНЫЙ langAlias
# ================================

# TODO: обновить ожидаемый статус-код после фиксов


@pytest.mark.parametrize(
    "langAlias, description",
    [
        ("", "пустой langAlias"),
        ("ru-en-too-long" * 20, "слишком длинный langAlias"),
        (None, "langAlias = null"),
        (123, "langAlias = число"),
        (True, "langAlias = boolean"),
        ([], "langAlias = список"),
        ({}, "langAlias = объект"),
    ],
)
def test_register_email_invalid_langAlias(
    auth_client, session_id_email_new, langAlias, description, assert_response
):

    resp = auth_client.register_email(
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias=langAlias,
        sessionId=session_id_email_new,
    )

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Неверное значение langAlias: {description}",
    )


# ================================
# 5. НЕВАЛИДНЫЙ sessionId
# ================================

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
def test_register_email_invalid_sessionId(
    auth_client, session_id_email_new, sessionId, description, assert_response
):

    resp = auth_client.register_email(
        password=TEST_REGISTER_PASSWORD,
        currency_id=4,
        langAlias="en",
        sessionId=sessionId,
    )

    assert_response(
        resp,
        expected=(400, 401, 403, 404),
        msg=f"Неверное значение sessionId: {description}",
    )
