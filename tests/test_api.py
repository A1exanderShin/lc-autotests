import requests

def test_login():
    response = requests.post("https://test2.lototeam.com/api/lotoclub_api/v1/auth/check_phone", json={"phone": "79061234567", "ip": "172.17.0.1", "platform": "web", "user_agent": "Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)"})
    assert response.status_code == 200
    assert "token" in response.json()