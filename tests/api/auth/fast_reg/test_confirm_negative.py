import pytest


@pytest.mark.parametrize(
    "session_id, description",
    [
        ("", "пустой sessionId"),
        (" " * 5, "sessionId из пробелов"),
        (123, "sessionId = int"),
        (True, "sessionId = boolean"),
        (None, "sessionId = null"),
        (["123123123123123"], "sessionId = список"),
        ({"id": "123123123123"}, "sessionId = объект"),
        ("😀😀😀", "sessionId = emoji"),
        ("1" * 5000, "слишком длинный sessionId"),
        ("00000000-0000-0000-0000-000000000000", "несуществующий sessionId"),
        ("not-a-uuid", "не uuid, но строка"),
    ],
)
def test_confirm_phone_negative(auth_client, session_id, description, assert_response):
    resp = auth_client.confirm_phone(session_id=session_id)
    assert_response(
        resp,
        expected=(400, 500),
        msg=f"Неверное значение sessionId: {description}",
    )
