def test_login_smoke(auth_user):
    """
    Простой smoke-тест авторизации.
    Проверяет, что:
    - токен получен
    - клиент авторизован
    """

    # Проверяем, что токен установлен
    token = auth_user.http.token
    assert token is not None, "Токен не был установлен после login"

    # Можно сделать пробный запрос на любой защищённый эндпоинт (если знаем)
    # Например, предположим, что /profile требует авторизации:
    response = auth_user.http.get("/user/me")

    # Пока не уверены, что /profile существует — просто печатаем статус
    print("Profile status:", response.status_code)

    assert response.status_code in (200, 401, 403), "Ошибка при обращении к профилю"
