import streamlit as st

def show_portfolio_table(df):
    st.subheader("📄 Dati del Portafoglio")
    st.dataframe(df[['name', 'ticker', 'type', 'quantity', 'price', 'value', 'currency', 'region', 'sector']], use_container_width=True)
