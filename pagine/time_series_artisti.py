from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

'''
In qeusto file è scritto il codice per la pagina della time series degli artisti
'''

# questa funzione avvia la pagina della 
# time series degli artisti
def run_time_series_artisti():
    
    # stampo il titolo e il logo di spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    serie = anal.time_series(df)
    st.title("Serie storica")
    
    # dizionario utlie
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
    st.title("Confronto serie storica divisa per artisti")
    stringaq = '''
        In questa sezione metteremo a confronto la serie storica degli artisti più ascoltati per vedere come sono cambiati nel tempo
        '''
    st.write(stringaq)
    
    # scrivo una funzione nel caso in cui la casella sia selezionata
    def not_ceck():
        oggi = datetime.now().date()
        anno_corrente = oggi.year
        n = st.slider(
            'Quanti artisti vuoi visualizzare?',
            min_value=1,
            max_value=10,
            value=3
        )

        # scelta del tipo di periodo
        opzione_periodo = st.radio(
            "Seleziona il periodo:",
            ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
        )

        # gestione del periodo in base alla selezione
        if opzione_periodo == "Dati di sempre":
            # uso l'intero range del DataFrame
            periodo = (df['ts'].min(), df['ts'].max())

        elif opzione_periodo == "Anno specifico":
            # permettono di scegliere un anno
            anno_selezionato = st.selectbox(
                "Seleziona un anno",
                [i for i in range(anno_corrente, anno_corrente - 11, -1)],
                index=0
            )
            periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, 12, 31))

        elif opzione_periodo == "Periodo personalizzato":
            # permetto di scegliere un intervallo di date
            start_date = st.date_input("Seleziona la data di inizio", value=datetime(anno_corrente, 1, 1).date())
            end_date = st.date_input("Seleziona la data di fine", value=oggi)
            if start_date > end_date:
                st.error("La data di inizio non può essere successiva alla data di fine.")
                return  # esce dalla funzione se l'intervallo non è valido
            periodo = (start_date, end_date)
        st.caption("Selezionando il periodo scegli di mettere a confronto la top n (numero selezionato con lo slider) artisti del periodo scelto")
        
        artisti_da_analizzare = anal.top_n_artisti(df, n, periodo)["master_metadata_album_artist_name"]
        artisti = []

        for i in artisti_da_analizzare:
            artisti.append(i)
            
        Tools.stampa_time_series_artisti(df, artisti, periodo)
        st.markdown("---")
        stringa1 = '''Per capire a che mese e che anno corrsisponde un certo periodo potete aiutarvi con lo slider qui sotto'''
        st.write(stringa1)
        periodo_richiesto = st.slider(
            'Che periodo ti interessa?',
            min_value=1,
            max_value=serie["periodo"][-1],
            value=1,
            key = "slider_2"
        )
        st.subheader(f"{mesi[serie["mese"][periodo_richiesto-1]]} {serie["anno"][periodo_richiesto-1]}")
        st.markdown("---")
    
    # scrivo una funzinoe nel caso in cui la casella NON sia selezionata
    def ceck():
            # calcolo del periodo massimo
            periodo = (df['ts'].min(), df['ts'].max())
            
            # ottengo gli artisti da analizzare
            artisti_da_analizzare = anal.top_n_artisti(df, periodo=periodo)["master_metadata_album_artist_name"]
            
            # selezione degli artisti da confrontare
            if "artisti" not in st.session_state:
                st.session_state.artisti = [i for i in artisti_da_analizzare]  # Memorizza la lista degli artisti
            
            artisti = st.session_state.artisti
            # multiselect per scegliere fino a 10 artisti
            selezione_artisti = st.multiselect(
                "Seleziona fino a 10 artisti da confrontare",
                artisti,  # lista degli artisti dal session_state
                default=st.session_state.get("selezione_artisti", []),  # Carica selezione precedente
                max_selections=10,
                key="multiselect_artisti"
            )
            
            # salvo le selezioni nel session_state
            if selezione_artisti:
                st.session_state["selezione_artisti"] = selezione_artisti
            else:
                st.warning("Seleziona almeno un artista!")


            if len(selezione_artisti) != 0:
                Tools.stampa_time_series_artisti(df, selezione_artisti, periodo)
                st.markdown("---")
                stringa1 = '''Per capire a che mese e che anno corrsisponde un certo periodo potete aiutarvi con lo slider qui sotto'''
                st.write(stringa1)
                periodo_richiesto = st.slider(
                    'Che periodo ti interessa?',
                    min_value=1,
                    max_value=serie["periodo"][-1],
                    value=1,
                    key = "slider_3"
                )
                st.subheader(f"{mesi[serie["mese"][periodo_richiesto-1]]} {serie["anno"][periodo_richiesto-1]}")
                st.markdown("---")

    st.write("Se vuoi scegliere manualmente gli artisti spunta la casella sottostante")
    if st.checkbox("Ciao io sono la casella"):
        ceck()
    else:
        not_ceck()
