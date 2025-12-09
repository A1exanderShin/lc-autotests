def test_fastreg_email_positive(fastreg_email_user):
    resp = fastreg_email_user.http.get("/user/me")
    assert resp.status_code == 200