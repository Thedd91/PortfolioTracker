# views/positions.py
import streamlit as st
import pandas as pd

# Dummy data for now (we'll connect to DB later)
POSITIONS = [
    {"Titolo": "Bitcoin", "Ticker": "BTC", "Quantità": 0.06, "Prezzo di acquisto": 2141.17, "Posizione attuale": 4453.92},
    {"Titolo": "Tesla", "Ticker": "TSLA", "Quantità": 6, "Prezzo di acquisto": 718.84, "Posizione attuale": 1271.25},
    {"Titolo": "Ethereum", "Ticker": "ETH", "Quantità": 0.5, "Prezzo di acquisto": 1552.67, "Posizione attuale": 1402.28},
    {"Titolo": "Microsoft", "Ticker": "MSFT", "Quantità": 2, "Prezzo di acquisto": 122.06, "Posizione attuale": 323.78},
]


def show_positions_view():
    st.subheader("📌 Posizioni")

    with st.expander("➕ Aggiungi nuova posizione"):
        col1, col2 = st.columns(2)
        with col1:
            titolo = st.text_input("Titolo")
            ticker = st.text_input("Ticker")
            quantity = st.number_input("Quantità", step=0.01, min_value=0.0)
        with col2:
            prezzo_acquisto = st.number_input("Prezzo di acquisto totale (EUR)", step=0.01, min_value=0.0)
            valore_attuale = st.number_input("Valore attuale (EUR)", step=0.01, min_value=0.0)

        if st.button("💾 Salva posizione"):
            POSITIONS.append({
                "Titolo": titolo,
                "Ticker": ticker,
                "Quantità": quantity,
                "Prezzo di acquisto": prezzo_acquisto,
                "Posizione attuale": valore_attuale
            })
            st.success(f"Posizione {titolo} salvata!")

    df = pd.DataFrame(POSITIONS)
    df["Totale acquisto"] = df["Prezzo di acquisto"]
    df["Totale attuale"] = df["Posizione attuale"]
    df["P/L (€)"] = df["Totale attuale"] - df["Totale acquisto"]
    df["P/L (%)"] = (df["P/L (€)"] / df["Totale acquisto"]) * 100

    st.dataframe(df.style.format({
        "Prezzo di acquisto": "{:.2f} €",
        "Posizione attuale": "{:.2f} €",
        "Totale acquisto": "{:.2f} €",
        "Totale attuale": "{:.2f} €",
        "P/L (€)": "{:+.2f} €",
        "P/L (%)": "{:+.2f}%"
    }), use_container_width=True)
