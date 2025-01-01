import streamlit as st
import Tools

def run_discover_artist():
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    
    titolo = st.text_input("Inserisci nome dell'artista")
    
    if titolo:
        Tools.stampa_info_artista(titolo)
    else:
        st.warning("Inserire il nome di un brano per avviare la ricerca")