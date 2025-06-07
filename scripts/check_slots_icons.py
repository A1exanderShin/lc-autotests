import psycopg2
import requests
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Подключение к БД (замени на свои данные)
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="db_game",
    user="postgres",
    password="Il0oi2ohgie1eigo"
)

with conn.cursor() as cursor:
    cursor.execute("SET search_path TO game;")
    cursor.execute("""
        SELECT provider_name, alias, game_name
        FROM game_slots
        WHERE api = 'mobule';
    """)
    games = cursor.fetchall()

conn.close()

size = "245-184"
extensions = ["png", "jpg", "jpeg", "svg"]
base_url = "https://cdn.effective-solution.com/CasinoMobule"

valid_links = []
invalid_links = []
games_without_images = []
image_report = []

MAX_WORKERS = 8
RETRIES = 2
DELAY_BETWEEN_RETRIES = 1  # секунда

def check_image_url_with_retries(url, ext):
    for attempt in range(1, RETRIES + 2):  # RETRIES+1 попыток всего
        try:
            response = requests.get(url, timeout=5, stream=True)
            if response.status_code == 200:
                return (url, ext, "found")
            elif response.status_code == 404:
                return (url, ext, "not_found")
            else:
                return (url, ext, f"error_{response.status_code}")
        except requests.RequestException:
            if attempt <= RETRIES:
                time.sleep(DELAY_BETWEEN_RETRIES)
                continue
            return (url, ext, "request_exception")

def process_game(game_tuple):
    provider, alias, name = game_tuple
    found_any = False
    safe_provider = quote(provider.strip())
    safe_alias = quote(alias.strip())

    slot_report_lines = [f"--- {name} ({provider}) ---"]
    print(f"Проверяю слот \"{name}\" ({provider})")

    results = []

    for ext in extensions:
        url = f"{base_url}/{safe_provider}/{size}/{safe_alias}.{ext}"
        result = check_image_url_with_retries(url, ext)
        results.append(result)

    for url, ext, status in results:
        if status == "found":
            valid_links.append(url)
            slot_report_lines.append(f"  [✅] {ext} - найдено: {url}")
            print(f"    [✅] {ext} - найдено")
            found_any = True
        elif status == "not_found":
            invalid_links.append(url)
            slot_report_lines.append(f"  [❌] {ext} - НЕ найдено: {url}")
            print(f"    [❌] {ext} - НЕ найдено")
        elif status.startswith("error_"):
            invalid_links.append(url)
            slot_report_lines.append(f"  [⚠️] {ext} - ошибка, статус {status[6:]}: {url}")
            print(f"    [⚠️] {ext} - ошибка, статус {status[6:]}")
        else:
            invalid_links.append(url)
            slot_report_lines.append(f"  [❌] {ext} - ошибка запроса: {url}")
            print(f"    [❌] {ext} - ошибка запроса")

    if not found_any:
        games_without_images.append(name)

    slot_report_lines.append("")
    return slot_report_lines

print(f"🔍 Проверяется {len(games)} игр по всем провайдерам\n")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_game = {executor.submit(process_game, game): game for game in games}
    for future in as_completed(future_to_game):
        image_report.extend(future.result())

# Сохраняем отчёты
with open("image_check_report.txt", "w", encoding="utf-8") as f_report:
    f_report.write("\n".join(image_report))

with open("found_image_links.txt", "w", encoding="utf-8") as f_found:
    for link in valid_links:
        f_found.write(link + "\n")

with open("not_found_image_links.txt", "w", encoding="utf-8") as f_not_found:
    for link in invalid_links:
        f_not_found.write(link + "\n")

with open("games_without_images.txt", "w", encoding="utf-8") as f_no_img:
    for game_name in games_without_images:
        f_no_img.write(game_name + "\n")

print("\n✅ Проверка завершена.")
print(f"Найдено картинок: {len(valid_links)}")
print(f"Не найдено картинок (ссылок): {len(invalid_links)}")
print(f"Слотов без картинок: {len(games_without_images)}")
