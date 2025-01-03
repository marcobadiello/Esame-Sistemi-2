import streamlit as st 
import Tools
def run_profilo():
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
    