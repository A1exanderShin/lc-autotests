import requests
from configuration import SERVICE_URL

def test_login():
    response = requests.post(url=SERVICE_URL, json={"phone": "79061234567", "ip": "172.17.0.1", "platform": "web", "user_agent": "Mozilla/5.0 (compatible; Konqueror/4.1; OpenBSD) KHTML/4.1.4 (like Gecko)"})
    assert response.status_code == 200
    assert "token" in response.json()