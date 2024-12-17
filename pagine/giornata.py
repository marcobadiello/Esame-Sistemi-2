from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

'''
In questo file c'è il codice per descrivere gli ascolti durante la gironatata
'''

def run_giornata():
    st.write("Giornata")
    orario_selezionato = st.slider(
        label="Seleziona orario",
        min_value=0,
        max_value=23,
        value=None
    )
    orari = {
    0: '00:00',
    1: '01:00',
    2: '02:00',
    3: '03:00',
    4: '04:00',
    5: '05:00',
    6: '06:00',
    7: '07:00',
    8: '08:00',
    9: '09:00',
    10: '10:00',
    11: '11:00',
    12: '12:00',
    13: '13:00',
    14: '14:00',
    15: '15:00',
    16: '16:00',
    17: '17:00',
    18: '18:00',
    19: '19:00',
    20: '20:00',
    21: '21:00',
    22: '22:00',
    23: '23:00'
}
    st.markdown(
    f"""
    <h1 style='text-align: center; color: white;'>
        {orari[orario_selezionato]}
    </h1>
    """,
    unsafe_allow_html=True
    )
    perc = anal.media_oraria(df)
    st.markdown(
    f"""
    <h1 style='text-align: center; color: white;'>
        {round(perc['observations'][orario_selezionato],3)}%
    </h1>
    """,
    unsafe_allow_html=True
    )
    
    Tools.grafico_giornata(df,orario_selezionato)
    Tools.grafico_giornata_orizzontale(df,orario_selezionato)
    
