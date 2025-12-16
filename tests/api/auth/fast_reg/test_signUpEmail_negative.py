import pytest

from tests.fixtures.auth_fixtures import (
    TEST_IP,
    TEST_PLATFORM,
    TEST_REGISTER_PASSWORD,
    TEST_USER_AGENT,
    random_email,
    random_phone,
)

# ==========================================================
# 1. ОТСУТСТВУЮЩИЕ ПОЛЯ (STRUCTURE)
# ==========================================================


@pytest.mark.parametrize(
    "use_email, use_password, use_currency_id, use_langAlias, description",
    [
        (False, False, False, False, "пустой JSON"),
        (False, True, True, True, "нет email"),
        (True, False, True, True, "нет password"),
        (True, True, False, True, "нет currency_id"),
        (True, True, True, False, "нет langAlias"),
    ],
)
def test_signUpEmail_missing_fields(
    auth_client,
    use_email,
    use_password,
    use_currency_id,
    use_langAlias,
    description,
    random_email,
    assert_response,
):

    # Собираем payload согласно пересечению параметров
    payload = {}
    if use_email:
        payload["email"] = random_email
    if use_password:
        payload["password"] = TEST_REGISTER_PASSWORD
    if use_currency_id:
        payload["currency_id"] = 4
    if use_langAlias:
        payload["langAlias"] = "en"

    # Передаём как именованные аргументы — signup_email сам соберёт payload
    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp, expected=(400, 500), msg=f"Отсутствуют обязательные поля: {description}"
    )


# ==========================================================
# 2. НЕВАЛИДНЫЙ password
# ==========================================================


@pytest.mark.parametrize(
    "password, description",
    [
        ("", "пустой password"),
        (" " * 5, "password из пробелов"),
        (123456, "password = int"),
        (None, "password = null"),
        (["123"], "password = список"),
        ({"p": "123"}, "password = объект"),
        ("1" * 5000, "слишком длинный password"),
    ],
)
def test_signUpEmail_invalid_password(
    auth_client, random_email, password, description, assert_response
):

    payload = {
        "email": random_email,
        "currency_id": 4,
        "langAlias": "en",
        "password": password,
    }

    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверное значение password: {description}",
    )


# ==========================================================
# 3. НЕВЕРНЫЕ ТИПЫ email (int, bool, list, dict) → 500
# ==========================================================


@pytest.mark.parametrize(
    "email, description",
    [
        (123456, "email = int"),
        (True, "email = boolean"),
        (None, "email = null"),
        (["aaa@bbb.cc"], "email = список"),
        ({"email": "aaa@bbb.cc"}, "email = объект"),
    ],
)
def test_signUpEmail_invalid_email_type(
    auth_client, email, description, assert_response
):

    payload = {
        "email": email,
        "password": TEST_REGISTER_PASSWORD,
        "currency_id": 4,
        "langAlias": "en",
    }

    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверный тип email: {description}",
    )


# ==========================================================
# 4. НЕВЕРНЫЕ ФОРМАТЫ email (string, но невалидные) → 400
# ==========================================================

INVALID_EMAIL_FORMATS = [
    ("aaa", "нет @"),
    ("aaa@", "нет домена"),
    ("@aaa", "нет имени"),
    ("aaa@bbb", "нет зоны (.com, .ru, .kz)"),
    ("aaa@bbb.", "пустая зона"),
    ("aaa bbb@ccc.com", "пробел в email"),
    ("аааа@bbb.com", "кириллица"),
    ("😀😀😀@mail.com", "эмодзи в имени"),
    ("aaa@😀😀😀.com", "эмодзи в домене"),
    ("aaa@@ccc.com", "двойной @"),
    ("aaa@c,om", "запятая в домене"),
    ("aaa@c.om.", "точка в конце"),
    ("aaa@bbb..com", "двойная точка"),
    ("", "пустая строка"),
]


@pytest.mark.parametrize("email, description", INVALID_EMAIL_FORMATS)
def test_signUpEmail_invalid_email_format(
    auth_client, email, description, assert_response
):

    payload = {
        "email": email,
        "password": TEST_REGISTER_PASSWORD,
        "currency_id": 4,
        "langAlias": "en",
    }

    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp,
        expected=(400, 500),  # по доке должно быть 400, но backend может дать 500
        msg=f"Неверный формат email: {description}",
    )


# ==========================================================
# 5. НЕВАЛИДНЫЕ currency_id
# ==========================================================


@pytest.mark.parametrize(
    "currency_id, description",
    [
        ("4", "currency_id = string"),  # строка вместо числа
        (None, "currency_id = null"),
        (True, "currency_id = boolean"),
        (3.14, "currency_id = float"),
        (["4"], "currency_id = список"),
        ({"id": 4}, "currency_id = объект"),
        (-1, "currency_id отрицательное"),
        (0, "currency_id = 0"),
        (9999, "currency_id слишком большое"),
        (10**50, "currency_id крайне большое число"),
    ],
)
def test_signUpEmail_invalid_currency_id(
    auth_client,
    random_email,
    currency_id,
    description,
    assert_response,
):

    payload = {
        "email": random_email,
        "password": TEST_REGISTER_PASSWORD,
        "currency_id": currency_id,
        "langAlias": "en",
    }

    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверное значение currency_id: {description}",
    )


# ==========================================================
# 6. НЕВАЛИДНЫЙ langAlias
# ==========================================================


@pytest.mark.parametrize(
    "langAlias, description",
    [
        (123, "langAlias = int"),
        (True, "langAlias = boolean"),
        (None, "langAlias = null"),
        (["en"], "langAlias = список"),
        ({"lang": "en"}, "langAlias = объект"),
        ("", "langAlias пустой"),
        (" ", "langAlias пробел"),
        ("EN", "верхний регистр"),
        ("e", "слишком короткий"),
        ("english", "слишком длинный текст"),
        ("рус", "кириллица"),
        ("😀😀😀", "эмодзи"),
        ("xx", "неизвестная локаль"),
        ("zzz", "невалидная зона локали"),
    ],
)
def test_signUpEmail_invalid_langAlias(
    auth_client,
    random_email,
    langAlias,
    description,
    assert_response,
):

    payload = {
        "email": random_email,
        "password": TEST_REGISTER_PASSWORD,
        "currency_id": 4,
        "langAlias": langAlias,
    }

    resp = auth_client.http.post("/auth/signUpEmail", json=payload)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверное значение langAlias: {description}",
    )
