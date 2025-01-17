import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df

def run_top_artisti():
    """
    Configura ed esegue la pagina Streamlit per visualizzare i migliori artisti di Spotify.
    Questa funzione imposta il layout della pagina, consente all'utente di selezionare il numero di artisti da visualizzare
    e scegliere il periodo di tempo per i dati. Successivamente, visualizza i migliori artisti in base ai criteri selezionati
    e mostra il periodo selezionato.
    L'utente può scegliere tra tre opzioni di periodo di tempo:
    - "Dati di sempre": Utilizza l'intero intervallo del dataframe.
    - "Anno specifico": Consente all'utente di selezionare un anno specifico.
    - "Periodo personalizzato": Consente all'utente di selezionare un intervallo di date personalizzato.
    La funzione include anche un footer con il nome del creatore.
    Ritorna:
        Nessuno
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
        'Quanti artisti vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )

    # scelta del tipo di periodo
    opzione_periodo = st.radio(
        "Seleziona il periodo:",
        ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
    )

    # gestisco il periodo in base alla selezione
    if opzione_periodo == "Dati di sempre":
        # utilizza l'intero range del dataframe
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
            return  # esce dalla funzione se l'intervallo non è valido
        periodo = (start_date, end_date)

    # mostro il periodo selezionato e i risultati
    Tools.stampa_top_artisti(df, n, periodo)
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

