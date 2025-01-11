import streamlit as st
import Tools

def run_discover_track():
    """
    Configura e avvia la pagina di scoperta brani in un'applicazione Streamlit.

    Questa funzione configura la pagina con un layout ampio e una barra laterale ridotta.
    Fornisce un input di testo per consentire all'utente di inserire il titolo di un brano. 
    Se viene inserito un titolo, chiama il metodo `stampa_info_track` dal modulo `Tools` per visualizzare 
    le informazioni relative al brano. Se non viene inserito un titolo, viene mostrato un messaggio di avviso 
    che invita l'utente a inserire il nome di un brano. Inoltre, aggiunge un footer alla pagina con il nome del creatore.

    Ritorna:
        Nessun valore (None).
    """
    # impostazioni della pagina
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    # scrivo il titolo
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    # strumento per selezionare brano
    titolo = st.text_input("Inserisci titolo del brano")
    if titolo:
        Tools.stampa_info_track(titolo)
    else:
        st.warning("Inserire il nome di un brano per avviare la ricerca")
    # footer
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