import streamlit as st
import Tools

def run_discover_artist():
    """
    Configura e avvia la pagina di scoperta artista in un'applicazione Streamlit.

    Questa funzione configura il layout della pagina con un layout ampio e una barra laterale ridotta per impostazione predefinita.
    Fornisce un input di testo per consentire all'utente di inserire il nome di un artista. Se viene inserito un nome, 
    chiama il metodo `stampa_info_artista` dal modulo `Tools` per visualizzare le informazioni relative all'artista. 
    Se non viene inserito un nome, viene mostrato un messaggio di avviso che invita l'utente a inserire il nome di un artista.
    Inoltre, aggiunge un footer alla pagina con il nome del creatore.

    Nota:
        La funzione presuppone che i moduli `st` (Streamlit) e `Tools` siano già importati.
    """
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    titolo = st.text_input("Inserisci nome dell'artista")
    if titolo:
        Tools.stampa_info_artista(titolo)
    else:
        st.warning("Inserire il nome di un artista per avviare la ricerca")
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