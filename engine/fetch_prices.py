import yfinance as yf
import requests

def get_price_yfinance(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Errore con {ticker} da yfinance: {e}")
        return None

def get_price_coingecko(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=eur"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return round(response.json()[symbol]['eur'], 2)
    except Exception as e:
        print(f"Errore con {symbol} da CoinGecko: {e}")
        return None
