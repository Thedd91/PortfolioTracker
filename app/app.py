# app/app.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# === Funzione per caricare dati dal DB ===
def load_portfolio_data():
    conn = sqlite3.connect("db/portfolio.db")
    df = pd.read_sql_query("SELECT * FROM portfolio_assets", conn)
    conn.close()
    return df

# === Layout Streamlit ===
st.set_page_config(page_title="Investment Tracker", layout="wide")
st.title("📊 Investment Tracker Dashboard")

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
