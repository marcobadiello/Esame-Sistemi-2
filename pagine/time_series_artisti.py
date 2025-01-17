from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

def run_time_series_artisti():
    """
    Questa funzione configura e avvia una pagina dell'app Streamlit per visualizzare i dati delle serie temporali della cronologia di ascolto degli artisti su Spotify.

    La funzione esegue le seguenti operazioni:
    1. Configura il layout della pagina Streamlit e lo stato della barra laterale.
    2. Visualizza il logo di Spotify e il titolo "Spotify Wrapped Statistico".
    3. Genera un'analisi delle serie temporali basata sul DataFrame fornito.
    4. Mostra un titolo e una descrizione per il confronto delle serie storiche suddivise per artisti.
    5. Fornisce opzioni per selezionare il numero di artisti da visualizzare e il periodo di analisi dei dati.
    6. Permette agli utenti di scegliere tra:
    - Visualizzare sempre i primi N artisti.
    - Selezionare manualmente fino a 10 artisti per il confronto.
    7. Visualizza i dati delle serie temporali per gli artisti e il periodo selezionati.
    8. Aggiunge un footer con il nome del creatore.

    La funzione include due sotto-funzioni principali:
    - `not_ceck()`: Gestisce il caso in cui l'utente non seleziona manualmente gli artisti.
    - `ceck()`: Gestisce il caso in cui l'utente seleziona manualmente gli artisti.

    Nota: La funzione si basa su moduli e funzioni esterne, come `anal.time_series`, `anal.top_n_artisti` e `Tools.stampa_time_series_artisti`.

    Ritorna:
    - Nessun valore (None).
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )

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
                

    st.write("Se vuoi scegliere manualmente gli artisti spunta la casella sottostante")
    if st.checkbox("Ciao io sono la casella"):
        ceck()
    else:
        not_ceck()
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
