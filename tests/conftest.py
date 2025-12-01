import pytest

pytest_plugins = [
    "tests.fixtures.auth_fixtures"
]

@pytest.fixture
def assert_response():
    def _assert(resp, expected=(200,), msg=""):
        assert resp.status_code in expected, (
            f"{msg} Ожидали {expected}, "
            f"но получили {resp.status_code}. Ответ: {resp.text}"
        )
    return _assert

