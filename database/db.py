import sqlite3

DB_PATH = "stocks.db"

def init_db():
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

def add_stock(user_id: int, ticker: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stocks (user_id, ticker) VALUES (?, ?)", (user_id, ticker.upper()))  

def get_stocks(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ticker FROM stocks WHERE user_id = ?", (user_id))   
        rows = cursor.fetchall()
        return [row[0] for row in rows]

def remove_stock(user_id: int, ticker: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE user_id = ? AND ticker = ?", (user_id, ticker.upper()))

def remove_all_stocks(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE user_id = ? ", (user_id))

    
