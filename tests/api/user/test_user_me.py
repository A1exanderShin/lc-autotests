from tests.fixtures.auth_fixtures import auth_client


def test_user_me_positive(auth_client, fastreg_phone_user):
    resp = fastreg_phone_user.http.get("/user/me")
    assert resp.status_code == 200