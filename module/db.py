import sqlite3
from pathlib import Path

DB_PATH = Path("reminder_users.db")

# Инициализация базы
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT
            )
        """)
        print("✅ База и таблица users инициализированы")

# Добавить или обновить пользователя
def save_user(user_id: int, full_name: str, username: str | None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO users (user_id, full_name, username)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                full_name=excluded.full_name,
                username=excluded.username
        """, (user_id, full_name, username))

# Получить всех пользователей
def get_all_users() -> list[tuple[int, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT user_id, full_name FROM users").fetchall()
        return rows
