import pytest

from tests.conftest import assert_response


# Token = None
def test_user_me_missing_token(auth_client, assert_response):
    resp = auth_client.http.get("/user/me")
    assert_response(resp, expected=(401, 403, 500), msg="Missing token")


def test_user_empty_token(auth_client, assert_response):
    auth_client.http.token = ""
    resp = auth_client.http.get("/user/me")
    assert_response(resp, expected=(401, 403, 500), msg="Empty token")


@pytest.mark.parametrize(
    "token, description",
    [
        ("123", "числа в строке"),
        ("abc", "буквы"),
        ("😀😀😀", "эмодзи"),
        ("wrong.token.value", "структура похожа, но не jwt"),
        ("@@@", "спецсимволы"),
        (" " * 5, "пробелы"),  # это можно оставить
        ("a" * 5000, "слишком длинный token"),
        ("bearer 123", "prefix bearer без jwt"),
    ],
)
def test_user_me_invalid_token(auth_client, assert_response, token, description):
    auth_client.http.token = token
    resp = auth_client.http.get("/user/me")
    assert_response(resp, expected=(401, 403, 500), msg=f"Invalid token: {description}")


@pytest.mark.parametrize(
    "corrupted, description",
    [
        (lambda t: t[:-1], "удалён последний символ"),
        (lambda t: ".".join(t.split(".")[:2]), "обрезан signature"),
        (lambda t: t.split(".")[0], "оставлен только header"),
        (lambda t: "a" + t, "добавлен символ в начало"),
        (lambda t: t[:10] + "a" + t[11:], "изменён символ в payload"),
    ],
)
def test_user_me_corrupted_jwt(
    fastreg_phone_user, assert_response, corrupted, description
):
    valid = fastreg_phone_user.http.token
    broken = corrupted(valid)
    fastreg_phone_user.http.token = broken
    resp = fastreg_phone_user.http.get("/user/me")
    assert_response(resp, expected=(401, 403, 500), msg=f"Corrupted JWT: {description}")


# TODO: Backend does not validate session context. Possible security issue.


def test_user_me_token_of_other_user(
    fastreg_phone_user, fastreg_email_user, assert_response
):
    token_B = fastreg_email_user.http.token
    fastreg_phone_user.http.token = token_B
    resp = fastreg_phone_user.http.get("/user/me")
    assert_response(resp, expected=(200, 401, 403, 500), msg="Token of another user")
