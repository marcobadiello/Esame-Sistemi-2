import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df
def run_top():
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )
    start_date = st.date_input("Seleziona la data di inizio", value=datetime(2022, 11, 1))
    end_date = st.date_input("Seleziona la data di fine", value=datetime(2023, 12, 31))
    periodo = (start_date,end_date)

    Tools.stampa_top_n(df,n,periodo)
