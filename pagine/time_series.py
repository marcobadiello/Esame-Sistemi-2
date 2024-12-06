from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
import Analisi as anal

def run_time_series():
    serie = anal.time_series(df)
    st.title("Serie storica")
    mesi = {
        1: "Gennaio",
        2: "Febbraio",
        3: "Marzo",
        4: "Aprile",
        5: "Maggio",
        6: "Giugno",
        7: "Luglio",
        8: "Agosto",
        9: "Settembre",
        10: "Ottobre",
        11: "Novembre",
        12: "Dicembre"
    }
    stringa = f'''
    Il seguente grafcio riporta la serie storica degli ascolti suddivisa per mesi. Ogni perido corrisponde a un mese a perire da {mesi[serie["month"][0]]} {serie["year"][0]} fino a 
    {mesi[serie["month"][-1]]} {serie["year"][-1]}
    '''
    st.write(stringa)
    Tools.stampa_time_series(df)
    st.markdown("---")
    stringa1 = '''Per capire a che mese e che anno corrsisponde un certo periodo potete aiutarvi con lo slider qui sotto'''
    st.write(stringa1)
    periodo_richiesto = st.slider(
        'Che periodo ti interessa?',
        min_value=1,
        max_value=serie["periodo"][-1],
        value=1
    )
    st.subheader(f"{mesi[serie["month"][periodo_richiesto-1]]} {serie["year"][periodo_richiesto-1]}")
    st.markdown("---")
    if st.button("Premimi per scoprire un segreto 🤫"):
        st.write("Il peridoo con il tempo di ascolto più alto è il perido 64 (più di 105 ore di ascolto) che corrsponde a Giugno 2023. Questo perchè il 3 Agosto 2023 ci sarebbe stato il concerto degli Imagine Dragons e io doveo ripassare le canzoni. Per questo c'è stato un picco nei miei ascolti.")
