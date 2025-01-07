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