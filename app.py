# app.py
import streamlit as st
from db.init import init_db, load_portfolio_data
from engine.update_db import update_prices_in_db

# Inizializza il DB (solo la prima volta o se mancante)
init_db()

st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

# Bottone per aggiornare i prezzi live
if st.button("🔄 Aggiorna prezzi live"):
    update_prices_in_db()
    st.success("Prezzi aggiornati con successo!")

# Carica i dati dal database
df = load_portfolio_data()

# Mostra valore totale del portafoglio
st.subheader("Valore totale del portafoglio")
total_value = df['current_value'].sum()
st.metric("Totale attuale (EUR)", f"{total_value:,.2f} €")

# Mostra la tabella delle posizioni
st.subheader("📊 Dettaglio posizioni")
st.dataframe(df.style.format({
    "current_price": "{:.2f} €",
    "total_cost": "{:.2f} €",
    "current_value": "{:.2f} €"
}), use_container_width=True)

