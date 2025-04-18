# views/allocation.py
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

def show_allocation_views(df):
    st.subheader("📍 Asset Allocation")

    # Inserisce una colonna mock 'region' se non presente
    if 'region' not in df.columns:
        regions = ['Europe', 'North America', 'Asia', 'Emerging Markets']
        df['region'] = np.random.choice(regions, size=len(df))

    # Filtra righe valide (valore > 0)
    df_valid = df[df['current_value'] > 0]

    if df_valid.empty:
        st.info("Nessun dato disponibile per creare la distribuzione regionale.")
    else:
        # Pie chart per regione
        fig_region = px.pie(
            df_valid,
            values='current_value',
            names='region',
            title='Distribuzione per Regione'
        )
        st.plotly_chart(fig_region, use_container_width=True)

        # Pie chart per asset type (ETF, crypto, ecc.)
        fig_type = px.pie(
            df_valid,
            values='current_value',
            names='asset_type',
            title='Distribuzione per Tipologia di Asset'
        )
        st.plotly_chart(fig_type, use_container_width=True)
