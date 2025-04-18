import streamlit as st
import plotly.express as px

def show_allocation_views(df):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌍 Allocation per Regione")
        fig_region = px.pie(df, values='value', names='region', title='Distribuzione per Regione')
        st.plotly_chart(fig_region, use_container_width=True)

    with col2:
        st.markdown("### 🏭 Allocation per Settore")
        fig_sector = px.pie(df, values='value', names='sector', title='Distribuzione per Settore')
        st.plotly_chart(fig_sector, use_container_width=True)
