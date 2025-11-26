import requests  # библиотека для HTTP-запросов
from typing import Optional, Dict  # типы для удобства и читаемости


class HttpBase:
    # Конструктор — вызывается при создании объекта клиента
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url  # базовый URL API (например: "https://stage.api.com")
        self.token = token  # токен пользователя, если он есть

    # Метод для сборки заголовков
    def build_headers(self, headers: Optional[Dict] = None) -> Dict:
        """
        Объединяет заголовки, переданные вручную, и добавляет токен, если он установлен.
        Возвращает финальный набор заголовков.
        """
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
        """
        Выполняет GET-запрос по указанному path.
        path — путь без base_url (например: "/auth/login")
        params — query-параметры (dict)
        headers — дополнительные заголовки
        """
        # Собираем полный URL
        url = self.base_url + path

        # Собираем финальные заголовки
        final_headers = self.build_headers(headers)

        # Лог простыми принтами (позже сделаем через logging)
        print(f"[GET] {url} params={params}")

        # Выполняем реальный HTTP GET-запрос
        response = requests.get(url, params=params, headers=final_headers)

        # Лог статуса ответа
        print(f"[GET] {url} → {response.status_code}")

        # Возвращаем response обратно в тесты
        return response

    # Метод POST-запроса
    def post(self, path: str, json: Dict | None = None, headers: Dict | None = None):
        """
        Выполняет POST-запрос.
        json — тело запроса в виде словаря (автоматически сериализуется в JSON)
        """
        # Формируем URL
        url = self.base_url + path

        # Формируем заголовки
        final_headers = self.build_headers(headers)

        # Логируем запрос
        print(f"[POST] {url} json={json}")

        # Отправляем POST-запрос
        response = requests.post(url, json=json, headers=final_headers)

        # Логируем результат
        print(f"[POST] {url} → {response.status_code}")

        # Возвращаем ответ
        return response
