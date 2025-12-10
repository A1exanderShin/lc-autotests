from src.clients.auth_client import AuthClient
from src.models.auth.password_recovery.send_mail import SendMailResponse
from tests.fixtures.auth_fixtures import BASE_URL


def test_send_mail_positive(auth_client, registered_user_email):
    email = registered_user_email.email

    # ВАЖНО: нужен новый клиент без токена!
    fresh_client = AuthClient(BASE_URL)

    resp = fresh_client.send_mail(email)

    assert isinstance(resp, SendMailResponse)
    assert resp.code == 200
    assert resp.status == "success"
    assert resp.sessionId
