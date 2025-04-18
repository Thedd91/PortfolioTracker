import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def show_performance_view(df):
    st.markdown("### 📈 Andamento storico (placeholder)")
    total_value = df['value'].sum()
    simulated_dates = pd.date_range(end=datetime.today(), periods=60)
    simulated_values = [total_value * (1 + 0.01 * ((i % 10) - 5)) for i in range(60)]
    fig_perf = go.Figure()
    fig_perf.add_trace(go.Scatter(x=simulated_dates, y=simulated_values, mode='lines', name='Valore Portafoglio'))
    fig_perf.update_layout(title='Simulazione Andamento Portafoglio (ultimi 60 giorni)', xaxis_title='Data', yaxis_title='Valore €')
    st.plotly_chart(fig_perf, use_container_width=True)
