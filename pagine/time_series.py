from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal


def run_time_series():
    st.set_page_config(layout="wide")
    # scrivo il titolo
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    serie = anal.time_series(df)
    st.title("Serie storica")
    # dizionario utile
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
    Il seguente grafcio riporta la serie storica degli ascolti suddivisa per mesi. 
    Ogni perido corrisponde a un mese a partire da {mesi[serie["mese"][0]]} {serie["anno"][0]} fino a 
    {mesi[serie["mese"][-1]]} {serie["anno"][-1]}
    '''
    st.write(stringa)
    # mostro a schermo la time series
    Tools.stampa_time_series(df)

    
    st.title("Serie storica cumulata")
    st.write("Il seguente grafcio mostra la serie storica cumulata degli ascolti, ad ongni periodo")
    # stampo la serie storica cumulata
    Tools.stampa_time_series_cumulata(df)
    # stampo lo slider
    
    
'''
COSE DA SAPERE
- Le key degli slideer sono tutte diverse perchè sennò mi creava problemi ma gli slider sono identici
'''