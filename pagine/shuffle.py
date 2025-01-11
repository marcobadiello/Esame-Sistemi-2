from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

def run_shuffle():
    """
    Configura e avvia la pagina Streamlit per visualizzare le statistiche relative alla funzione shuffle di Spotify.

    La funzione imposta il layout della pagina, visualizza il logo di Spotify e il titolo, fornisce una descrizione delle statistiche sulla funzione shuffle e mostra un grafico a torta con i dati percentuali relativi all'utilizzo della funzione shuffle. Include anche un'opzione per gli utenti daltonici per modificare i colori del grafico.

    La pagina include:
    - Logo di Spotify e titolo
    - Descrizione delle statistiche sulla funzione shuffle
    - Checkbox per modificare i colori del grafico per utenti daltonici
    - Grafico a torta che mostra le statistiche di utilizzo della funzione shuffle
    - Percentuali relative all'utilizzo della funzione shuffle
    - Footer con il nome del creatore

    Nota:
    - La funzione presuppone l'esistenza di un DataFrame `df` e dei moduli `Tools` e `anal` con i metodi `stmapa_torta_shuffle` e `shuffle_data` rispettivamente.

    Ritorna:
    - Nessun valore (None).
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )

    # metto il titolo e il logo di spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    
    stringa = '''
    In questa pagina puoi vedere un grafico che mostra quanto viene utilizzato 
    in percentuale la funzione 'Shuffle', ovvero la riproduzione casuale.
    '''
    colori = ("#00FF00", "#FF0000")
    if st.checkbox("Sono daltonico"):
        colori = ("#0055FF"," #FFDD00")
    st.write(stringa)
    Tools.stmapa_torta_shuffle(df,colori=colori)
    data = anal.shuffle_data(df)
    col1, col2 = st.columns([2,2])
    with col1:
        st.markdown(
    f"""
    <h1 style='text-align: center; color: {colori[0]};'>
        {round((round(data[3],3)*100),3)}%
    </h1>
    """,
    unsafe_allow_html=True
    )
    with col2:
        st.markdown(
    f"""
    <h1 style='text-align: center; color: {colori[1]};'>
        {round((round(data[4],3)*100),3)}%
    </h1>
    """,
    unsafe_allow_html=True
    )
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
        


    