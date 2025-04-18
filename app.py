# app.py

import streamlit as st
from views.positions import show_positions_view
from views.performance import show_performance_view
from views.portfolio_table import show_portfolio_table
from views.allocation import show_allocation_views
from db.init import init_db, load_portfolio_data

# === Configurazione layout Streamlit ===
st.set_page_config(page_title="Investment Tracker", layout="wide")
st.title("📊 Investment Tracker Dashboard")

# === Inizializza il database se necessario ===
init_db()
df = load_portfolio_data()

# === Riepilogo portafoglio ===
st.subheader("💰 Valore totale portafoglio")
total_value = df['value'].sum()
st.metric(label="Valore totale attuale", value=f"{total_value:,.2f} €")

# === Visualizzazioni modulari ===
show_performance_view(df)
show_positions_view()
show_allocation_views(df)
