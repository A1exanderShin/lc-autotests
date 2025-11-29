# ✔ Полный список негативных тестов для test_login_negative.py
# 🔥 1. НЕВЕРНЫЙ ПАРОЛЬ
# Неверный пароль (WRONG)
# Пароль правильный по формату, но неверный (например, "123456789")
# Пароль содержит мусор ("!@#$%^&*()")
#
# 🔥 2. ПУСТЫЕ ЗНАЧЕНИЯ
# Пустой пароль (password="")
# Пустой sessionId (sessionId="")
# Оба поля пустые (password="", sessionId="")
#
# 🔥 3. НЕВЕРНЫЙ sessionId
# sessionId со случайными символами ("123-abc")
# sessionId слишком короткий ("1" или "abc")
# sessionId слишком длинный (100+ символов)
# sessionId = None (если API позволяет такое отправить)
# sessionId неверного типа (integer вместо строки)
#
# 🔥 4. НЕВЕРНЫЙ ТИП ДАННЫХ
# password = None
# password = integer
# password = массив (list)
# sessionId = integer
# sessionId = объект (dict)
# (Если backend отдаёт 400 — значит, валидация работает.)
#
# 🔥 5. Логин без предварительного check_email
# login_email вызывается с НЕ тем sessionId, например sessionId от phone
# login_email вызывается со старым sessionId, который уже невалиден
# (если API поддерживает такую проверку)
#
# 🔥 6. Некорректная структура запроса
# Отправить запрос БЕЗ поля "password"
# Отправить запрос БЕЗ поля "sessionId"
# Отправить пустое тело {}
# (Это важно — часто ломает API.)
#
# 🔥 7. SQL/инъекции и мусор
# Пароль = " OR 1=1 --"
# Пароль = "DROP TABLE users"
# Пароль = "😀😀😀"
# (Валидация не обязана ловить, но важный негатив.)





# ПУСТЫЕ ЗНАЧЕНИЯ
def test_login_email_empty_password(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="",
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_empty_sessionId(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=""
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )

def test_login_email_empty_all(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="",
        sessionId=""
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )





# НЕКОРРЕКТНАЯ СТРУКТУРА ЗАПРОСА
def test_login_email_without_password(auth_client, session_id_email):
    resp = auth_client.http.post("/auth/email_login", json={
        "sessionId": session_id_email
    })

    assert resp.status_code in (400, 401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_without_sessionId(auth_client, session_id_email):
    resp = auth_client.http.post("/auth/email_login", json={
        "password": "123123123"
    })

    assert resp.status_code in (400, 401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )

def test_login_email_without_all(auth_client, session_id_email):
    resp = auth_client.http.post("/auth/email_login", json={})

    assert resp.status_code in (400, 401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )




# НЕВЕРНЫЕ ЗНАЧЕНИЯ И ТИПЫ
def test_login_email_wrong_password_boolean(auth_client, session_id_email):
    resp = auth_client.login_email(
        password=True,
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_password_int(auth_client, session_id_email):
    resp = auth_client.login_email(
        password=123123123,
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_password_none(auth_client, session_id_email):
    resp = auth_client.login_email(
        password=None,
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_password_list(auth_client, session_id_email):
    resp = auth_client.login_email(
        password=["123123123"],
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_password_dict(auth_client, session_id_email):
    resp = auth_client.login_email(
        password={"password": "123123123"},
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_password_emoji(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="😀😀😀",
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_long_password(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="1" * 5000,
        sessionId=session_id_email
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_boolean(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=True
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_int(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=123123123
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_none(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=None
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_list(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId=[session_id_email]
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_dict(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId={"sessionId": session_id_email}
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_wrong_sessionId_emoji(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId="😀😀😀"
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )


def test_login_email_long_sessionId(auth_client, session_id_email):
    resp = auth_client.login_email(
        password="123123123",
        sessionId="1" * 5000
    )

    assert resp.status_code in (400,401), (
        f"Ожидали 400/401, но получили {resp.status_code}. Ответ: {resp.text}"
    )
