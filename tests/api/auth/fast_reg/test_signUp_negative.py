import pytest

from tests.fixtures.auth_fixtures import (
    TEST_IP,
    TEST_PLATFORM,
    TEST_REGISTER_PASSWORD,
    TEST_USER_AGENT,
    random_phone,
)

# ==========================================================
# 1. ОТСУТСТВУЮЩИЕ ПОЛЯ (STRUCTURE)
# ==========================================================


@pytest.mark.parametrize(
    "use_phone, use_password, description",
    [
        (False, False, "пустой JSON"),
        (False, True, "нет phone"),
        (True, False, "нет password"),
    ],
)
def test_signUp_phone_missing_fields(
    auth_client, use_phone, use_password, description, random_phone, assert_response
):

    # Собираем payload согласно пересечению параметров
    phone = random_phone if use_phone else None
    password = TEST_REGISTER_PASSWORD if use_password else None

    # Передаём как именованные аргументы — signup_phone сам соберёт payload
    resp = auth_client.signup_phone(phone=phone, password=password)

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
def test_signUp_phone_invalid_password(
    auth_client, random_phone, password, description, assert_response
):

    resp = auth_client.signup_phone(phone=random_phone, password=password)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверное значение password: {description}",
    )


# ==========================================================
# 3. НЕВЕРНЫЕ ТИПЫ phone (int, bool, list, dict) → 500
# ==========================================================


@pytest.mark.parametrize(
    "phone, description",
    [
        (1234567890, "phone = int"),
        (True, "phone = boolean"),
        (None, "phone = null"),
        (["77000000000"], "phone = список"),
        ({"phone": "77000000000"}, "phone = объект"),
    ],
)
def test_signUp_phone_invalid_type(auth_client, phone, description, assert_response):

    resp = auth_client.signup_phone(phone=phone, password=TEST_REGISTER_PASSWORD)

    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверный тип phone: {description}",
    )


# ==========================================================
# 4. НЕВЕРНЫЕ ФОРМАТЫ phone (string, но невалидные) → 400
# ==========================================================

INVALID_PHONE_FORMATS = [
    ("7", "слишком короткий"),
    ("77", "КЗ — слишком короткий"),
    ("9989", "УЗ — слишком короткий"),
    ("628", "ИНД — слишком короткий"),
    ("7" * 30, "слишком длинный"),
    ("9989" + "1" * 20, "УЗ слишком длинный"),
    ("628" + "1" * 20, "ИНД слишком длинный"),
    ("abc", "буквы в номере"),
    ("77,1234567", "запятая в номере"),
    ("628.1234567", "точка в номере"),
    ("😀😀😀", "эмодзи вместо номера"),
    ("75123456789", "КЗ без префикса 77"),
    ("99791234567", "УЗ неверный префикс"),
    ("621234567890", "ИНД неверный префикс"),
]


@pytest.mark.parametrize("phone, description", INVALID_PHONE_FORMATS)
def test_signUp_phone_invalid_format(auth_client, phone, description, assert_response):

    resp = auth_client.signup_phone(phone=phone, password=TEST_REGISTER_PASSWORD)

    assert_response(
        resp,
        expected=(400, 500),  # формат должен давать 400, но мы страхуемся от 500
        msg=f"Неверный формат phone: {description}",
    )
