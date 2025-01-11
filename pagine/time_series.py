from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

def run_time_series():
    """
    Configura e visualizza una pagina Streamlit con l'analisi delle serie temporali dei dati di ascolto su Spotify.

    La funzione esegue i seguenti compiti:
    1. Configura la pagina con un layout ampio e una barra laterale ridotta.
    2. Visualizza il logo di Spotify e il titolo "Spotify Wrapped Statistico".
    3. Genera e mostra un grafico a serie temporali dei dati di ascolto su Spotify.
    4. Fornisce una descrizione del grafico a serie temporali, compreso l'intervallo temporale e la sua utilità.
    5. Mostra un grafico cumulativo delle serie temporali dei dati di ascolto su Spotify.
    6. Fornisce una descrizione del grafico cumulativo e della sua utilità.
    7. Aggiunge un footer con il nome del creatore.

    La funzione utilizza le seguenti funzioni e variabili esterne:
    - `anal.time_series(df)`: Genera i dati delle serie temporali.
    - `Tools.stampa_time_series(df)`: Mostra il grafico delle serie temporali.
    - `Tools.stampa_time_series_cumulata(df)`: Mostra il grafico cumulativo delle serie temporali.

    Nota:
    - La funzione presume che il DataFrame `df` sia già definito e contenga i dati necessari.
    - Si presume che il modulo `st` (Streamlit) sia già importato.
    - Si presume che i moduli `anal` e `Tools` siano già importati.
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )

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
    {mesi[serie["mese"][-1]]} {serie["anno"][-1]}. Questo grafico è utile per verificare l'andametno degli ascolti 
    nel tempo e per vedere eventuali stagionalità
    '''
    st.write(stringa)
    # mostro a schermo la time series
    Tools.stampa_time_series(df)

    
    st.title("Serie storica cumulata")
    st.write("Il seguente grafcio mostra la serie storica cumulata degli ascolti, ad ongni periodo. Questo grafico è utile per vdedere eventuali bruschi aumenti di ascolto nel tempo o periodo di bassi ascolti.")
    # stampo la serie storica cumulata
    Tools.stampa_time_series_cumulata(df)
    st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
    Creato con ❤️ da <b>Marco Badiello</b>
    </div>
    """,
    unsafe_allow_html=True
)
