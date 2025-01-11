import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df
import Analisi as anal

def run_top_canzoni():
    """
    Configura e avvia l'app Streamlit per visualizzare le canzoni più ascoltate su Spotify.

    La funzione include le seguenti funzionalità:
    - Configurazione della pagina con layout ampio e barra laterale ridotta.
    - Visualizzazione del logo di Spotify e del titolo dell'app.
    - Slider per scegliere il numero di canzoni da mostrare.
    - Checkbox per filtrare le canzoni per artista.
    - Pulsanti radio per selezionare il periodo di analisi (tutti i dati, anno specifico o periodo personalizzato).
    - Input per le date per selezionare un intervallo personalizzato.
    - Multiselezione per scegliere fino a 10 artisti da confrontare.
    - Visualizzazione delle canzoni principali basata sui filtri e sul periodo selezionato.
    - Footer con informazioni sul creatore dell'app.

    Nota:
    - La funzione presuppone la presenza di un DataFrame `df` contenente i dati di Spotify, con una colonna 'ts' che rappresenta i timestamp.
    - Utilizza funzioni esterne come `anal.top_n_artisti` e `Tools.stampa_top_canzoni_n` per l'elaborazione e la visualizzazione dei dati.

    Ritorna:
    - Nessun valore (None).
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )

    oggi = datetime.now().date()
    anno_corrente = oggi.year
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")

    # slider per scegliere il numero di canzoni
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )
    
    if st.checkbox("Filtra per artisti"):
        
        
        # scelta del periodo
        opzione_periodo = st.radio(
            "Seleziona il periodo:",
            ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
        )

        # gestisco il periodo in base alla selezione
        if opzione_periodo == "Dati di sempre":
            # utilizzo l'intero range del dataframe
            periodo = (df['ts'].min(), df['ts'].max())

        elif opzione_periodo == "Anno specifico":
            # permetto di scegliere un anno
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
                return  # esco dalla funzione se l'intervallo non è valido
            periodo = (start_date, end_date)
            

            
        # ottengo gli artisti da analizzare
        artisti_da_analizzare = anal.top_n_artisti(df, periodo=periodo)["master_metadata_album_artist_name"]
            
        # selezione degli artisti da confrontare
        if "artisti" not in st.session_state:
            st.session_state.artisti = [i for i in artisti_da_analizzare]  # Memorizza la lista degli artisti
            
        artisti = st.session_state.artisti
        # multiselect per scegliere fino a 10 artisti
        selezione_artisti = st.multiselect(
            "Seleziona fino a 10 artisti",
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
            Tools.stampa_top_canzoni_n(df, n, periodo,artisti = selezione_artisti)
                
    else:
        # scelta del periodo
        opzione_periodo = st.radio(
            "Seleziona il periodo:",
            ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
        )

        # gestisco il periodo in base alla selezione
        if opzione_periodo == "Dati di sempre":
            # utilizzo l'intero range del dataframe
            periodo = (df['ts'].min(), df['ts'].max())

        elif opzione_periodo == "Anno specifico":
            # permetto di scegliere un anno
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
                return  # esco dalla funzione se l'intervallo non è valido
            periodo = (start_date, end_date)

        # mostro a schermo il periodo e i risultati ottenuti
        Tools.stampa_top_canzoni_n(df, n, periodo)
        st.write(f"Periodo selezionato: da {periodo[0].strftime('%Y-%m-%d')} a {periodo[1].strftime('%Y-%m-%d')}")
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

