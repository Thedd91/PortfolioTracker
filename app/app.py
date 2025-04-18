# app/app.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
import yfinance as yf

# === Crea database e dati demo se non esistono ===
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
    # Verifica se ci sono dati
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
                st.error(f"Errore durante il fetch di {ticker}: {e}")
    conn.commit()
    conn.close()

# === Funzione per caricare dati dal DB ===
def load_portfolio_data():
    conn = sqlite3.connect("portfolio.db")
    df = pd.read_sql_query("SELECT * FROM portfolio_assets", conn)
    conn.close()
    return df

# === Layout Streamlit ===
st.set_page_config(page_title="Investment Tracker", layout="wide")
st.title("📊 Investment Tracker Dashboard")

# === Inizializzazione DB se necessario ===
init_db()

# === Caricamento dati ===
df = load_portfolio_data()

# === Tabella principale ===
st.subheader("📄 Dati del Portafoglio")
st.dataframe(df[['name', 'ticker', 'type', 'quantity', 'price', 'value', 'currency', 'region', 'sector']], use_container_width=True)

# === Visualizzazioni ===
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌍 Allocation per Regione")
    fig_region = px.pie(df, values='value', names='region', title='Distribuzione per Regione')
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.markdown("### 🏭 Allocation per Settore")
    fig_sector = px.pie(df, values='value', names='sector', title='Distribuzione per Settore')
    st.plotly_chart(fig_sector, use_container_width=True)

# === Altre visualizzazioni future: currency exposure, performance, ecc ===
# Verranno aggiunte nei moduli successivi
