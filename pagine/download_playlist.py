import streamlit as st
import Tools

def run_dawnload_playlist():
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