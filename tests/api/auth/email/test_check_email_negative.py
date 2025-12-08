import pytest

from tests.fixtures.auth_fixtures import TEST_IP, TEST_USER_AGENT, TEST_EMAIL

# НЕПОЛНЫЙ JSON
@pytest.mark.parametrize("payload,description", [
    ({"ip": TEST_IP, "user_agent":TEST_USER_AGENT}, "Нет email"),
    ({"email": TEST_EMAIL, "user_agent":TEST_USER_AGENT}, "Нет ip"),
    ({"email": TEST_EMAIL, "ip": TEST_IP,}, "Нет user-agent"),
    ({}, "Пустой JSON")
])
def test_check_email_missing_fields(auth_client, assert_response, payload, description):
    resp = auth_client.http.post("/auth/check_email", json=payload)

    assert_response(resp, expected=(400, 404), msg=f"Отсутствуют обязательные поля: ({description})")



# НЕВЕРНЫЕ ЗНАЧЕНИЯ ПОЛЕЙ
@pytest.mark.parametrize("email,description", [
    ("a",                   "слишком короткий"),
    ("aaa",                 "нет домена"),
    ("a@",                  "нет домена после @"),
    ("aaa@aaa",             "нет точки в домене"),
    ("aaa@aaa.",            "точка на конце"),
    ("aaa@aaa,aaa",         "запятая вместо точки"),
    ("😀😀😀",             "редкие символы - смайлики"),
    ("a"*300 + "@test.com", "слишком длинный email"),

    (123,                   "число вместо email"),
    ({"value": 123},                 "объект вместо email"),
    ([123],                 "список вместо email"),
    (None,                  "null email"),
    (False,                 "boolean-значение вместо email"),
    ("",                    "пустой email"),
])
def test_check_email_invalid_email(auth_client, assert_response, email, description):
    resp = auth_client.check_email(
        email=email,
        ip=TEST_IP,
        user_agent=TEST_USER_AGENT
    )

    assert_response(resp, expected=(400,), msg=f"Неверный формат email: ({description})")

@pytest.mark.parametrize("ip,description", [
    ("999.999.999.999", "невалидный ipv4"),
    ("test",            "строка без формата ip"),
    (123,               "число вместо ip"),
    ({"value": 123},    "объект вместо ip"),
    ([123],             "список вместо ip"),
    (None,              "null ip"),
    (False,             "boolean-значение вместо ip"),
    ("",                "пустой ip")
])
def test_check_email_invalid_ip(auth_client, assert_response, ip, description):
    resp = auth_client.check_email(
        email=TEST_EMAIL,
        ip=ip,
        user_agent=TEST_USER_AGENT
    )

    assert_response(resp, expected=(400,), msg=f"Неверный формат ip: ({description})")

@pytest.mark.parametrize("user_agent,description", [
    (123,               "число вместо user-agent"),
    ({"value": 123},    "объект вместо user-agent"),
    ([123],             "список вместо user-agent"),
    (None,              "null user-agent"),
    (False,             "boolean-значение вместо user-agent"),
    ("",                "пустой user-agent"),
])
def test_check_email_invalid_user_agent(auth_client, assert_response, user_agent, description):
    resp = auth_client.check_email(
        email=TEST_EMAIL,
        ip=TEST_IP,
        user_agent=user_agent
    )

    assert_response(resp, expected=(400,), msg=f"Неверный формат user-agent: ({description})")