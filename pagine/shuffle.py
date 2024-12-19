from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

'''
In questo file c'è il codicce per la pagina streamlit realativa
ai dati riguardo l'utilizzo della modalità di shuffle
'''

def run_shuffle():
    # metto il titolo e il logo di spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    
    stringa = '''
    In questa pagina puoi vedere un grafico che mostra quanto viene utilizzato 
    in percentuale la funzione 'Shuffle', ovvero la riproduzione casuale
    '''
    st.write(stringa)
    Tools.stmapa_torta_shuffle(df)
    data = anal.shuffle_data(df)
    col1, col2 = st.columns([2,2])
    with col1:
        st.markdown(
    f"""
    <h1 style='text-align: center; color: #00FF00;'>
        {round(data[3], 3)*100}%
    </h1>
    """,
    unsafe_allow_html=True
    )
    with col2:
        st.markdown(
    f"""
    <h1 style='text-align: center; color: #FF0000;'>
        {round(data[4], 3)*100}%
    </h1>
    """,
    unsafe_allow_html=True
    )