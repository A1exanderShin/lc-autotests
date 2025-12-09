import pytest

from tests.fixtures.auth_fixtures import (
    TEST_IP,
    TEST_USER_AGENT,
    TEST_PHONE,
    TEST_PLATFORM,
)

INVALID_PHONES = [

    # --- A. Длина ---
    ("7", "слишком короткий"),
    ("77", "слишком короткий (КЗ)"),
    ("9989", "слишком короткий (УЗ)"),
    ("628", "слишком короткий (ИНД)"),

    ("7" * 30, "слишком длинный"),
    ("9989" + "1" * 20, "слишком длинный УЗ"),
    ("628" + "1" * 20, "слишком длинный ИНД"),

    # --- B. Формат ---
    ("a", "буква вместо цифр"),
    ("aaa", "несколько букв"),
    ("abc123", "смешанные буквы/цифры"),
    ("+-()123", "спецсимволы"),
    ("😀😀😀", "эмодзи"),
    ("77,1234567", "запятая в номере"),
    ("628.1234567", "точка в номере"),

    # --- C. Неверные типы ---
    (77000000000, "число вместо строки"),
    (["77000000000"], "список вместо строки"),
    ({"phone": "77000000000"}, "объект вместо строки"),
    (True, "boolean вместо строки"),
    (None, "null phone"),
    ("", "пустая строка"),

    # --- D. Нарушение префикса ---
    ("75123456789", "КЗ без префикса 77"),
    ("99791234567", "УЗ неправильный код (нет 9987/9988/9989)"),
    ("621234567890", "ИНД должен начинаться с 628"),

    # --- E. Похожие, но невалидные ---
    ("779999", "похож на КЗ, но слишком короткий"),
    ("99851234567", "УЗ неверный подпрефикс"),
    ("6271234567", "ИНД неверный подпрефикс"),
]

INVALID_PLATFORMS = [

    # --- Типы ---
    (123, "число вместо platform"),
    (True, "boolean вместо platform"),
    (None, "null platform"),
    (["android"], "список вместо строки"),
    ({"p": "android"}, "объект вместо строки"),

    # --- Форматы ---
    ("", "пустая строка"),
    ("   ", "строка из пробелов"),
    ("😀😀😀", "эмодзи"),
    ("@@@", "спецсимволы"),
    ("verylongplatformname" * 5, "слишком длинная строка"),
    # --- Неизвестные значения ---
    ("windows_phone", "несуществующая платформа"),
    ("smart_toaster", "мусорное значение"),
]


# =======================================================
#   Т Е С Т Ы   Н Е П О Л Н О Г О   J S O N
# =======================================================

# TODO: обновить ожидаемый статус-код после фиксов

@pytest.mark.parametrize("payload,description", [
    ({"ip": TEST_IP, "user_agent": TEST_USER_AGENT, "platform": TEST_PLATFORM}, "Нет phone"),
    ({"phone": TEST_PHONE, "user_agent": TEST_USER_AGENT, "platform": TEST_PLATFORM}, "Нет ip"),
    ({"phone": TEST_PHONE, "ip": TEST_IP, "platform": TEST_PLATFORM}, "Нет user-agent"),
    ({"phone": TEST_PHONE, "ip": TEST_IP, "user_agent": TEST_USER_AGENT}, "Нет platform"),
    ({}, "Пустой JSON"),
])
def test_check_phone_missing_fields(auth_client, assert_response, payload, description):
    resp = auth_client.http.post("/auth/check_phone", json=payload)

    assert_response(resp, expected=(200, 400, 401, 403, 404), msg=f"Отсутствуют обязательные поля: ({description})")


# =======================================================
#   П Р О В Е Р К А   Н Е В Е Р Н О Г О   PHONE
# =======================================================

# TODO: обновить ожидаемый статус-код после фиксов

@pytest.mark.parametrize("phone,description", INVALID_PHONES)
def test_check_phone_invalid_phone(auth_client, assert_response, phone, description):
    resp = auth_client.check_phone(
        phone=phone,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT,
    )

    assert_response(
        resp,
        expected=(400, 401, 500),
        msg=f"Неверный формат phone: {description}"
    )


# =======================================================
#   П Р О В Е Р К А   Н Е В Е Р Н О Г О   IP
# =======================================================

# TODO: обновить ожидаемый статус-код после фиксов

@pytest.mark.parametrize("ip,description", [
    ("999.999.999.999", "невалидный ipv4"),
    ("test", "строка без формата ip"),
    (123, "число вместо ip"),
    ({"value": 123}, "объект вместо ip"),
    ([123], "список вместо ip"),
    (None, "null ip"),
    (False, "boolean ip"),
    ("", "пустой ip"),
])
def test_check_phone_invalid_ip(auth_client, assert_response, ip, description):
    resp = auth_client.check_phone(
        phone=TEST_PHONE,
        ip=ip,
        platform=TEST_PLATFORM,
        user_agent=TEST_USER_AGENT,
    )

    assert_response(
        resp,
        expected=(200, 400, 401, 403, 404),
        msg=f"Неверный формат ip: {description}"
    )


# =======================================================
#   П Р О В Е Р К А   Н Е В Е Р Н О Г О   PLATFORM
# =======================================================

# TODO: обновить ожидаемый статус-код после фиксов

@pytest.mark.parametrize("platform,description", INVALID_PLATFORMS)
def test_check_phone_invalid_platform(auth_client, assert_response, platform, description):
    resp = auth_client.check_phone(
        phone="77123456789",   # гарантированно валидный номер КЗ
        ip=TEST_IP,
        platform=platform,
        user_agent=TEST_USER_AGENT,
    )

    assert_response(
        resp,
        expected=(200, 400, 401, 403, 404),
        msg=f"Неверный формат platform: {description}"
    )


# =======================================================
#   П Р О В Е Р К А   Н Е В Е Р Н О Г О   USER-AGENT
# =======================================================

# TODO: обновить ожидаемый статус-код после фиксов

@pytest.mark.parametrize("user_agent,description", [
    (123, "число вместо user-agent"),
    ({"value": 123}, "объект вместо user-agent"),
    ([123], "список вместо user-agent"),
    (None, "null user-agent"),
    (False, "boolean user-agent"),
    ("", "пустой user-agent"),
])
def test_check_phone_invalid_user_agent(auth_client, assert_response, user_agent, description):
    resp = auth_client.check_phone(
        phone=TEST_PHONE,
        ip=TEST_IP,
        platform=TEST_PLATFORM,
        user_agent=user_agent,
    )

    assert_response(
        resp,
        expected=(200, 400, 401, 403, 404),
        msg=f"Неверный формат user-agent: {description}"
    )
