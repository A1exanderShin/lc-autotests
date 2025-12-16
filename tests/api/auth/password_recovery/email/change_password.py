from src.clients.auth_client import AuthClient
from tests.fixtures.auth_fixtures import BASE_URL


def test_change_password_email_positive(
    password_recovery_email_session
):
    session_id = password_recovery_email_session

    guest = AuthClient(BASE_URL)

    resp = guest.change_password_email(
        session_id=session_id,
        password="NewPassword123!"
    )

    assert resp.code == 200
    assert resp.status == "success"
