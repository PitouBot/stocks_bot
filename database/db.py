import sqlite3
import logging


logger = logging.getLogger(__name__)
DB_PATH = "stocks.db"

def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                ticker TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")

def add_stock(user_id: int, ticker: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO stocks (user_id, ticker) VALUES (?, ?)", (user_id, ticker.upper()))  
    except Exception as e:
        logger.error(f"Ошибка добавления {ticker}: {e}")

def get_stocks(user_id: int):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ticker FROM stocks WHERE user_id = ?", (user_id))   
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        logger.error(f"Ошибка получения акций: {e}")
        return []
      

def remove_stock(user_id: int, ticker: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE user_id = ? AND ticker = ?", (user_id, ticker.upper()))
    except Exception as e:
        logger.error(f"Ошибка удаления {ticker}: {e}")

def remove_all_stocks(user_id: int):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE user_id = ? ", (user_id))
    except Exception as e:
        logger.error(f"Ошибка удаления всех акций: {e}")

    
