import sqlite3
import pandas as pd
from datetime import datetime
import yfinance as yf

def init_db():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ticker TEXT,
            type TEXT,
            region TEXT,
            sector TEXT,
            currency TEXT,
            quantity REAL,
            price REAL,
            value REAL,
            last_updated TEXT
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM portfolio_assets")
    if cursor.fetchone()[0] == 0:
        etf_data = {
            'IWDA.AS': {
                'name': 'iShares MSCI World',
                'region': 'Global',
                'sector': 'Mixed',
                'currency': 'EUR',
                'type': 'ETF',
                'quantity': 10
            },
            'SAD1.DE': {
                'name': 'iShares MSCI EM',
                'region': 'Emerging Markets',
                'sector': 'Mixed',
                'currency': 'EUR',
                'type': 'ETF',
                'quantity': 8
            }
        }
        for ticker, data in etf_data.items():
            try:
                yf_data = yf.Ticker(ticker)
                price = yf_data.info.get('regularMarketPrice', 0)
                value = price * data['quantity']
                last_updated = datetime.now().isoformat()
                cursor.execute('''
                    INSERT INTO portfolio_assets 
                    (name, ticker, type, region, sector, currency, quantity, price, value, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['name'], ticker, data['type'], data['region'], data['sector'],
                    data['currency'], data['quantity'], price, value, last_updated
                ))
            except Exception as e:
                print(f"Errore durante il fetch di {ticker}: {e}")
    conn.commit()
    conn.close()

def load_portfolio_data():
    conn = sqlite3.connect("portfolio.db")
    df = pd.read_sql_query("SELECT * FROM portfolio_assets", conn)
    conn.close()
    return df
