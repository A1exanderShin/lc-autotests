import allure
import requests  # библиотека для HTTP-запросов
from typing import Optional, Dict  # типы для удобства и читаемости


class HttpBase:
    # Конструктор — вызывается при создании объекта клиента
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url  # базовый URL API (например: "https://stage.api.com")
        self.token = token  # токен пользователя, если он есть

    # Метод для сборки заголовков
    def build_headers(self, headers: Optional[Dict] = None) -> Dict:
        # Если передали headers → копируем их; если нет → создаём пустой словарь
        final_headers = headers.copy() if headers else {}

        # Если клиент авторизован и есть токен → добавляем в заголовки
        if self.token:
            final_headers["X-Access-Token"] = self.token

        # По умолчанию указываем, что отправляем JSON (если клиент этого не сделал раньше)
        final_headers.setdefault("Content-Type", "application/json")

        # Возвращаем итоговый набор заголовков
        return final_headers

    # Метод GET-запроса
    def get(self, path: str, params: Dict | None = None, headers: Dict | None = None):
        url = self.base_url + path
        final_headers = self.build_headers(headers)

        with allure.step(f"GET {url}"):
            if params:
                allure.attach(str(params), "Request Params", allure.attachment_type.TEXT)

            response = requests.get(url, params=params, headers=final_headers)

            allure.attach(response.text, "Response JSON", allure.attachment_type.JSON)

            return response

    # Метод POST-запроса
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

