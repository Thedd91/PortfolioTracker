import sqlite3
from engine.fetch_prices import get_price_yfinance, get_price_coingecko

DB_PATH = "db/portfolio.db"


def update_prices_in_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id, ticker, asset_type FROM assets")
    assets = c.fetchall()

    for asset_id, ticker, asset_type in assets:
        if asset_type in ["etf", "stock"]:
            price = get_price_yfinance(ticker)
        elif asset_type == "crypto":
            price = get_price_coingecko(ticker)
        else:
            price = None

        if price:
            c.execute("""
                UPDATE assets
                SET current_price = ?
                WHERE id = ?
            """, (price, asset_id))
            print(f"✔️ {ticker} aggiornato a {price} EUR")
        else:
            print(f"❌ {ticker}: prezzo non aggiornato")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_prices_in_db()
