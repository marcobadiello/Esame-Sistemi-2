import streamlit as st 
import Tools

def run_profilo():
    """
    Configura e avvia la pagina del profilo Streamlit per Spotify Wrapped Statistico.

    La funzione esegue le seguenti operazioni:
    1. Configura la pagina con un layout ampio e una barra laterale ridotta.
    2. Visualizza il logo di Spotify e il titolo della pagina.
    3. Chiama `Tools.stampa_profilo()` per visualizzare le informazioni del profilo dell'utente.
    4. Aggiunge un divisore e un titolo per la sezione delle preferenze musicali.
    5. Mostra una breve descrizione della sezione.
    6. Fornisce uno slider per consentire all'utente di selezionare il numero di canzoni e artisti da visualizzare.
    7. Fornisce un pulsante radio per permettere all'utente di selezionare il periodo di interesse.
    8. Chiama `Tools.stampa_top_profilo(n, periodo)` per visualizzare le canzoni e gli artisti principali in base al periodo selezionato.
    9. Aggiunge un footer con il nome del creatore.

    Nota:
    - Si presuppone che i moduli `st` e `Tools` siano già importati e disponibili nel contesto.
    """

    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    Tools.stampa_profilo()
    st.divider()
    st.title("Panoramica dei gusti musicali")
    testo = '''
    In questa sezione puoi vedere un semplice e breve riassunto dei tuoi artisti e delle tue canzoni preferite a breve, medio e lungo termine
    '''
    st.subheader(testo)
    n = st.slider("Quante canzoni e artisti vuoi visualizzare ?",min_value=1,max_value=50)


    # Lista di opzioni
    opzioni = ["Lungo termine (1 anno)", "Medio termine (6 mesi)", "Breve termine (4 settimane)"]

    # Creazione di un componente radio
    scelta = st.radio("Seleziona il periodo di interesse:", opzioni)
    if scelta == "Lungo termine (1 anno)":
        periodo = 'long_term'
    elif scelta == "Medio termine (6 mesi)":
        periodo = 'medium_term'
    elif scelta == "Breve termine (4 settimane)":
        periodo = 'short_term'
    Tools.stampa_top_profilo(n,periodo)
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
    