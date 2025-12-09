def test_fastreg_phone_positive(fastreg_phone_user):
    resp = fastreg_phone_user.http.get("/user/me")
    assert resp.status_code == 200
