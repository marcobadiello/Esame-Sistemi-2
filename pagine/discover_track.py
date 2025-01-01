import streamlit as st
import Tools

def run_discover_track():
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    
    titolo = st.text_input("Inserisci titolo del brano")
    
    if titolo:
        Tools.stampa_info_track(titolo)
    else:
        st.warning("Inserire il nome di un brano per avviare la ricerca")