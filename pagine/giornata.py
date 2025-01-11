from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

def run_giornata():
    """
    Configura e avvia la pagina Streamlit per visualizzare le statistiche di ascolto su Spotify durante il giorno.

    La pagina include:
    - Un titolo e il logo di Spotify.
    - Un'introduzione che spiega lo scopo della pagina.
    - Uno slider per selezionare una specifica ora del giorno.
    - Visualizzazione dell'ora selezionata e della percentuale di ascolto corrispondente.
    - Un grafico circolare che mostra la distribuzione dell'ascolto durante la giornata.
    - Un grafico orizzontale per la variazione dettagliata dell'ascolto.
    - Un grafico cumulativo della percentuale per l'intera giornata.
    - Un footer con il nome del creatore.

    Utilizza le seguenti funzioni esterne:
    - `anal.media_oraria(df)`: Calcola la percentuale media di ascolto per ogni ora.
    - `Tools.grafico_giornata(df, orario_selezionato)`: Genera un grafico circolare per l'ora selezionata.
    - `Tools.grafico_giornata_orizzontale(df, orario_selezionato)`: Genera un grafico orizzontale per l'ora selezionata.
    - `Tools.grafico_giornata_orizzontale_cumulato(df, orario_selezionato)`: Genera un grafico orizzontale cumulativo per l'intera giornata.

    Nota:
    - La funzione presuppone l'esistenza di un DataFrame `df` contenente i dati necessari.
    - La funzione utilizza Streamlit per l'interfaccia web.
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
    # scrivo il titolo
    st.title("Percentuale di ascolto durante la giornata")
    # scrivo una introduzione
    stringa = '''
    In questa pagina puoi vedere come varia l'ascolto della musica durante
    l'arco della giornata, tutti i valori riportati sono in percentuale rispetto a tutta la musica ascoltata.
    Per vedere i dati di un orario particolare utilizza lo slieder qui sotto.
    '''
    st.write(stringa)
    # creo uno slider per selezionare l'orario
    orario_selezionato = st.slider(
        label="Seleziona un orario",
        min_value=0,
        max_value=23,
        value=12
    )
    # dizionario utile
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
    # mostro orario selezionato
    st.markdown(
    f"""
    <h1 style='text-align: center; color: #FF0000;'>
        {orari[orario_selezionato]}
    </h1>
    """,
    unsafe_allow_html=True
    )
    perc = anal.media_oraria(df)
    # mostro percentuale relativa all'orario selezionato
    st.markdown(
    f"""
    <h1 style='text-align: center; color: #FF0000;'>
        {round(perc['observations'][orario_selezionato],3)}%
    </h1>
    """,
    unsafe_allow_html=True
    )
    # mostro il grafico circolare
    aa = '''
    In questo grafico puoi avere una visione degli ascolti durante i vari momenti della giornata.
    '''
    st.write(aa)
    Tools.grafico_giornata(df,orario_selezionato)
    # mostro il grafico orizzonale
    bb = '''
    In questo grafico puoi vedere più dettagliatamente come i tuoi ascolti variano durante la giornata.
    '''
    st.write(bb)
    Tools.grafico_giornata_orizzontale(df,orario_selezionato)
    

    st.title("Percentuale di ascolto cumulata durante la giornata")
    stringhetta = '''
    In qeusto grafico puoi vedere la percentuale cumualta dell'ascolto di musica
    durante la giornata per vedere se ci sono incrementi repentini che segnalano un forte aumento
    di ascolti o momenti più piatti dove gli ascolti sono pochi.
    '''
    st.write(stringhetta)
    Tools.grafico_giornata_orizzontale_cumulato(df,orario_selezionato)  
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