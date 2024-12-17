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
    <h1 style='text-align: center; color: white;'>
        {orari[orario_selezionato]}
    </h1>
    """,
    unsafe_allow_html=True
    )
    perc = anal.media_oraria(df)
    # mostro percentuale relativa all'orario selezionato
    st.markdown(
    f"""
    <h1 style='text-align: center; color: white;'>
        {round(perc['observations'][orario_selezionato],3)}%
    </h1>
    """,
    unsafe_allow_html=True
    )
    # mostro il grafico circolare
    Tools.grafico_giornata(df,orario_selezionato)
    # mostro il grafico orizzonale
    Tools.grafico_giornata_orizzontale(df,orario_selezionato)
    

    st.title("Percentuale di ascolto cumulata durante la giornata")
    stringhetta = '''
    In qeusto grafico puoi vedere la percentuale cumualta dell'ascolto di musica
    durante la giornata per vedere se ci sono incrementi repentini che segnalano un forte aumento
    di ascolti o momenti più piatti dove gli ascolti sono pochi.
    '''
    st.write(stringhetta)
    Tools.grafico_giornata_orizzontale_cumulato(df,orario_selezionato)  