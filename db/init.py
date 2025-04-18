# db/init.py
import sqlite3
import os

DB_PATH = "db/portfolio.db"

ASSETS_SCHEMA = """
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    asset_type TEXT CHECK(asset_type IN ('stock', 'etf', 'crypto')),
    current_price REAL DEFAULT 0
);
"""

TRANSACTIONS_SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    price REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(asset_id) REFERENCES assets(id)
);
"""

def init_db():
    if not os.path.exists("db"):
        os.makedirs("db")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(ASSETS_SCHEMA)
    c.execute(TRANSACTIONS_SCHEMA)
    conn.commit()
    conn.close()

def load_portfolio_data():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("""
        SELECT a.id, a.ticker, a.asset_type, a.current_price,
               IFNULL(SUM(t.quantity), 0) as total_quantity,
               IFNULL(SUM(t.quantity * t.price), 0) as total_cost,
               IFNULL(SUM(t.quantity), 0) * a.current_price as current_value
        FROM assets a
        LEFT JOIN transactions t ON a.id = t.asset_id
        GROUP BY a.id
    """).fetchall()
    cols = ["id", "ticker", "asset_type", "current_price", "quantity", "total_cost", "current_value"]
    conn.close()
    import pandas as pd
    return pd.DataFrame(df, columns=cols)
