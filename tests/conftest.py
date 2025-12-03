import pytest

from src.models.auth.common.errors import ErrorResponse
from tests.fixtures.auth_fixtures import *


@pytest.fixture
def assert_response():
    def _assert(resp, expected=(200,), msg=""):

        # -----------------------------
        # 1. Pydantic ErrorResponse
        # -----------------------------
        if isinstance(resp, ErrorResponse):
            assert resp.code in expected, (
                f"{msg} Ожидали {expected}, "
                f"но получили {resp.code}. Ответ: {resp}"
            )
            return resp

        # -----------------------------
        # 2. Успешная Pydantic модель (есть .code, нет .status_code)
        # -----------------------------
        if hasattr(resp, "code") and not hasattr(resp, "status_code"):
            assert resp.code in expected, (
                f"{msg} Ожидали {expected}, "
                f"но получили {resp.code}. Ответ: {resp}"
            )
            return resp

        # -----------------------------
        # 3. Обычный requests.Response
        # -----------------------------
        status = resp.status_code
        text = getattr(resp, "text", "")
        assert status in expected, (
            f"{msg} Ожидали {expected}, но получили {status}. Ответ: {text}"
        )

        return resp

    return _assert
