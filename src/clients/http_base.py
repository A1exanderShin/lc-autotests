import allure
import requests
from typing import Optional, Dict


class HttpBase:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url  # базовый URL API (например: "https://stage.api.com")
        self.token = token  # токен пользователя, если он есть

    def build_headers(self, headers: Optional[Dict] = None) -> Dict:
        final_headers = headers.copy() if headers else {}

        if self.token:
            final_headers["X-Access-Token"] = self.token

        final_headers.setdefault("Content-Type", "application/json")

        return final_headers


    def get(self, path: str, params: Dict | None = None, headers: Dict | None = None):
        url = self.base_url + path
        final_headers = self.build_headers(headers)

        with allure.step(f"GET {url}"):
            if params:
                allure.attach(str(params), "Request Params", allure.attachment_type.TEXT)

            response = requests.get(url, params=params, headers=final_headers)

            allure.attach(response.text, "Response JSON", allure.attachment_type.JSON)

            return response


    def post(self, path: str, json: Dict | None = None, headers: Dict | None = None):
        url = self.base_url + path
        final_headers = self.build_headers(headers)

        with allure.step(f"POST {url}"):
            if json is not None:
                allure.attach(str(json), "Request JSON", allure.attachment_type.JSON)

            response = requests.post(url, json=json, headers=final_headers)

            try:
                allure.attach(response.text, "Response JSON", allure.attachment_type.JSON)
            except:
                pass

            return response

