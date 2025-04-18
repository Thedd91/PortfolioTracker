# app.py
import streamlit as st
from db.init import init_db, load_portfolio_data
from engine.update_db import update_prices_in_db
from views.positions import show_positions_view
from views.allocation import show_allocation_views
from views.performance import show_performance_view
import plotly.express as px
import pandas as pd

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

# Andamento temporale sintetico (mock temporaneo)
with st.expander("📉 Andamento storico del portafoglio (placeholder)"):
    # Simulazione andamento temporale fittizio (da sostituire con storico reale)
    mock_data = pd.DataFrame({
        "Data": pd.date_range(end=pd.Timestamp.today(), periods=10),
        "Valore": [total_value * (0.95 + 0.01 * i) for i in range(10)]
    })
    fig = px.line(mock_data, x="Data", y="Valore", title="Andamento del portafoglio")
    st.plotly_chart(fig, use_container_width=True)

# Mostra la tabella delle posizioni
st.subheader("📊 Dettaglio posizioni")
st.dataframe(df.style.format({
    "current_price": "{:.2f} €",
    "total_cost": "{:.2f} €",
    "current_value": "{:.2f} €"
}), use_container_width=True)

# Visualizzazioni aggiuntive
st.markdown("---")
show_positions_view()
show_allocation_views(df)
show_performance_view(df)
