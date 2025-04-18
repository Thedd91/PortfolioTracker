# views/performance.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def show_performance_view(df):
    st.subheader("📈 Andamento storico (placeholder)")

    # Correggi colonna: 'value' -> 'current_value'
    total_value = df['current_value'].sum()

    # Crea dati storici simulati
    mock_data = pd.DataFrame({
        "Data": pd.date_range(end=datetime.today(), periods=10),
        "Valore": [total_value * (0.95 + 0.01 * i) for i in range(10)]
    })

    fig = px.line(mock_data, x="Data", y="Valore", title="Andamento del Portafoglio nel tempo")
    st.plotly_chart(fig, use_container_width=True)
