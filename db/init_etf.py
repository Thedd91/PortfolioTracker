# db/init_etf.py
import sqlite3

# Connessione al DB
conn = sqlite3.connect("db/portfolio.db")
cursor = conn.cursor()

# Caricamento schema ETF
with open("db/schema/etf_schema.sql", "r") as f:
    cursor.executescript(f.read())

# Funzione per inserire ETF con dati statici

def insert_etf(isin, name, ticker, currency, ter, current_price, sectors, regions, holdings):
    cursor.execute("""
    INSERT OR IGNORE INTO etf (isin, name, ticker, currency, ter, current_price)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (isin, name, ticker, currency, ter, current_price))

    etf_id = cursor.lastrowid or cursor.execute("SELECT id FROM etf WHERE isin = ?", (isin,)).fetchone()[0]

    cursor.executemany("INSERT INTO etf_sectors (etf_id, sector, percent) VALUES (?, ?, ?)",
                       [(etf_id, s, p) for s, p in sectors])
    cursor.executemany("INSERT INTO etf_regions (etf_id, region, percent) VALUES (?, ?, ?)",
                       [(etf_id, r, p) for r, p in regions])
    cursor.executemany("""
    INSERT INTO etf_holdings (etf_id, stock_name, stock_ticker, weight, country, sector, industry)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(etf_id, *h) for h in holdings])

# ETF MSCI World (IE00B4L5Y983)
insert_etf(
    "IE00B4L5Y983",
    "iShares Core MSCI World UCITS ETF",
    "IWDA",
    "EUR",
    0.20,
    41.32,
    [
        ("Information Technology", 22.7), ("Financials", 14.6), ("Health Care", 12.8),
        ("Industrials", 11.4), ("Consumer Discretionary", 10.9), ("Communication", 7.3),
        ("Consumer Staples", 7.0), ("Energy", 4.6), ("Materials", 3.9),
        ("Utilities", 2.7), ("Real Estate", 2.1)
    ],
    [
        ("United States", 68.1), ("Japan", 6.4), ("United Kingdom", 4.0),
        ("France", 3.5), ("Canada", 3.2), ("Switzerland", 3.1),
        ("Germany", 2.5), ("Australia", 2.2), ("Netherlands", 1.3),
        ("Others", 5.7)
    ],
    [
        ("Apple", "AAPL", 4.81, "USA", "Information Technology", "Consumer Electronics"),
        ("Microsoft", "MSFT", 3.65, "USA", "Information Technology", "Software"),
        ("NVIDIA", "NVDA", 2.91, "USA", "Information Technology", "Semiconductors"),
        ("Amazon", "AMZN", 2.45, "USA", "Consumer Discretionary", "E-commerce"),
        ("Meta", "META", 1.94, "USA", "Communication", "Social Media"),
        ("Alphabet A", "GOOGL", 1.85, "USA", "Communication", "Search Engine"),
        ("Alphabet C", "GOOG", 1.72, "USA", "Communication", "Search Engine"),
        ("Tesla", "TSLA", 1.61, "USA", "Consumer Discretionary", "Automotive"),
        ("UnitedHealth", "UNH", 1.55, "USA", "Health Care", "Health Insurance"),
        ("JPMorgan", "JPM", 1.44, "USA", "Financials", "Banking"),
        ("Johnson & Johnson", "JNJ", 1.39, "USA", "Health Care", "Pharmaceuticals"),
        ("Visa", "V", 1.32, "USA", "Financials", "Payments"),
        ("Eli Lilly", "LLY", 1.26, "USA", "Health Care", "Pharmaceuticals"),
        ("ASML", "ASML", 1.18, "Netherlands", "Information Technology", "Semiconductors"),
        ("Broadcom", "AVGO", 1.14, "USA", "Information Technology", "Semiconductors"),
        ("Mastercard", "MA", 1.10, "USA", "Financials", "Payments"),
        ("Nestle", "NESN", 1.02, "Switzerland", "Consumer Staples", "Food"),
        ("Procter & Gamble", "PG", 0.98, "USA", "Consumer Staples", "Consumer Goods"),
        ("Novo Nordisk", "NOVO-B", 0.94, "Denmark", "Health Care", "Pharmaceuticals"),
        ("Home Depot", "HD", 0.91, "USA", "Consumer Discretionary", "Retail"),
        ("Samsung", "005930.KQ", 0.88, "South Korea", "Information Technology", "Electronics"),
        ("Toyota", "7203.T", 0.85, "Japan", "Consumer Discretionary", "Automotive"),
        ("Chevron", "CVX", 0.83, "USA", "Energy", "Oil & Gas"),
        ("Roche", "ROG", 0.80, "Switzerland", "Health Care", "Pharmaceuticals"),
        ("ExxonMobil", "XOM", 0.77, "USA", "Energy", "Oil & Gas")
    ]
)

# Secondo ETF: MSCI Emerging Markets (EIMI)
insert_etf(
    "IE00B0M62Y33",
    "iShares Core MSCI Emerging Markets IMI UCITS ETF",
    "EIMI",
    "USD",
    0.18,
    26.45,
    [
        ("Financials", 21.2), ("Information Technology", 18.3), ("Consumer Discretionary", 13.1),
        ("Materials", 8.8), ("Industrials", 7.6), ("Communication", 7.2),
        ("Energy", 6.1), ("Consumer Staples", 5.9), ("Utilities", 5.2),
        ("Real Estate", 3.5), ("Health Care", 3.1)
    ],
    [
        ("China", 29.7), ("India", 18.0), ("Taiwan", 14.9), ("South Korea", 12.6),
        ("Brazil", 5.2), ("South Africa", 3.9), ("Saudi Arabia", 3.1),
        ("Thailand", 1.8), ("Mexico", 1.6), ("Others", 9.2)
    ],
    [
        ("Taiwan Semi.", "TSMC", 6.1, "Taiwan", "Information Technology", "Semiconductors"),
        ("Samsung", "005930.KQ", 4.8, "South Korea", "Information Technology", "Electronics"),
        ("Tencent", "0700.HK", 4.1, "China", "Communication", "Internet"),
        ("Alibaba", "9988.HK", 3.7, "China", "Consumer Discretionary", "E-commerce"),
        ("Reliance Ind.", "RELIANCE.NS", 2.8, "India", "Energy", "Conglomerate"),
        ("Meituan", "3690.HK", 2.1, "China", "Consumer Discretionary", "Online Services"),
        ("Vale", "VALE3.SA", 1.9, "Brazil", "Materials", "Mining"),
        ("Infosys", "INFY.NS", 1.8, "India", "Information Technology", "IT Services"),
        ("Saudi Aramco", "2222.SR", 1.7, "Saudi Arabia", "Energy", "Oil & Gas"),
        ("Naspers", "NPN.JO", 1.5, "South Africa", "Communication", "Media"),
        ("ICICI Bank", "ICICIBC.NS", 1.4, "India", "Financials", "Banking"),
        ("China Const. Bank", "0939.HK", 1.3, "China", "Financials", "Banking"),
        ("JD.com", "9618.HK", 1.2, "China", "Consumer Discretionary", "E-commerce"),
        ("Petrobras", "PETR4.SA", 1.1, "Brazil", "Energy", "Oil & Gas"),
        ("FEMSA", "FMX", 1.0, "Mexico", "Consumer Staples", "Beverages")
    ]
)

conn.commit()
conn.close()
print("✅ ETF inseriti con successo")
