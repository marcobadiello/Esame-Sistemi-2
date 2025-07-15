import streamlit as st
import Tools
import Analisi as anal
from credenziali import client_id
from credenziali import client_secret
from credenziali import redirect_uri
from Estrattore import df

def run_dawnload_coperine():
    
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    # scrivo un aspegazione di cosa fa il programma dopo
    st.title("Scarica copertine canzoni")
    st.write(f"Questo programma scarica le copertine delle canzoni da Spotify in base agli URI presenti nel file di analisi. Totale {len(anal.get_codici(df))}")
    # faccio un bottone che avvia una funzione
    if st.button("Scarica copertine canzoni"):
        Tools.scarica_copertine_da_uri_list(anal.get_codici(df), client_id, client_secret)
