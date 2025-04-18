# views/allocation.py
import streamlit as st
import plotly.express as px
import numpy as np

def show_allocation_views(df):
    st.subheader("📍 Asset Allocation")

    # Inserisce una colonna mock 'region' se non presente
    if 'region' not in df.columns:
        regions = ['Europe', 'North America', 'Asia', 'Emerging Markets']
        df['region'] = np.random.choice(regions, size=len(df))

    # Pie chart per regione
    fig_region = px.pie(
        df,
        values='current_value',
        names='region',
        title='Distribuzione per Regione'
    )
    st.plotly_chart(fig_region, use_container_width=True)

    # Pie chart per asset type (ETF, crypto, ecc.)
    fig_type = px.pie(
        df,
        values='current_value',
        names='asset_type',
        title='Distribuzione per Tipologia di Asset'
    )
    st.plotly_chart(fig_type, use_container_width=True)
