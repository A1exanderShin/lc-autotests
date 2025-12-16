from src.clients.auth_client import AuthClient
from tests.fixtures.auth_fixtures import BASE_URL


def test_confirm_mail_code_positive(registered_user_email):
    email = registered_user_email.email

    guest = AuthClient(BASE_URL)

    send_resp = guest.send_mail(email)
    assert send_resp.code == 200

    confirm_resp = guest.confirm_mail_code(
        mailCode="111111",
        sessionId=send_resp.sessionId
    )

    assert confirm_resp.code == 200
    assert confirm_resp.status == "success"
