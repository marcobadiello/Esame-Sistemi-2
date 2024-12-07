from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
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
    Il seguente grafcio riporta la serie storica degli ascolti suddivisa per mesi. Ogni perido corrisponde a un mese a perire da {mesi[serie["mese"][0]]} {serie["anno"][0]} fino a 
    {mesi[serie["mese"][-1]]} {serie["anno"][-1]}
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
    st.subheader(f"{mesi[serie["mese"][periodo_richiesto-1]]} {serie["anno"][periodo_richiesto-1]}")
    st.markdown("---")

    st.title("Confronto serie storica divisa per artisti")
    stringaq = '''
    In questa sezione metteremo a confronto la serie storica degli artisti più ascoltati per vedere come sono cambiati nel tempo
    '''
    st.write(stringaq)
    oggi = datetime.now().date()
    anno_corrente = oggi.year
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=10,
        value=3
    )
    opzione_periodo = st.radio(
        "Seleziona il periodo:",
        ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
    )

    # Gestione del periodo in base alla selezione
    if opzione_periodo == "Dati di sempre":
        # Usa l'intero range del DataFrame
        periodo = (df['ts'].min(), df['ts'].max())

    elif opzione_periodo == "Anno specifico":
        # Permetti di scegliere un anno
        anno_selezionato = st.selectbox(
            "Seleziona un anno",
            [i for i in range(anno_corrente, anno_corrente - 11, -1)],
            index=0
        )
        periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, 12, 31))

    elif opzione_periodo == "Periodo personalizzato":
        # Permetti di scegliere un intervallo di date
        start_date = st.date_input("Seleziona la data di inizio", value=datetime(anno_corrente, 1, 1).date())
        end_date = st.date_input("Seleziona la data di fine", value=oggi)
        if start_date > end_date:
            st.error("La data di inizio non può essere successiva alla data di fine.")
            return  # Esce dalla funzione se l'intervallo non è valido
        periodo = (start_date, end_date)
        
    artisti_da_analizzare = anal.top_n_artisti(df,n,periodo)["master_metadata_album_artist_name"]
    st.write(artisti_da_analizzare)