import streamlit as st
import Tools

def run_dawnload_playlist():
    """
    Configura e avvia l'app Streamlit per il download di una playlist Spotify.

    Questa funzione configura il layout della pagina, inclusi la disposizione e lo stato della barra laterale.
    Visualizza il logo di Spotify e il titolo "Spotify Wrapped Statistico" in un layout a due colonne.
    Successivamente, chiama il metodo `stampa_dawnload_palylist` dal modulo `Tools` per gestire il download della playlist.
    Infine, aggiunge un footer alla pagina con il nome del creatore.

    Nota:
    - La funzione presuppone che i moduli `st` (Streamlit) e `Tools` siano già importati.
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
    Tools.stampa_dawnload_palylist()
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