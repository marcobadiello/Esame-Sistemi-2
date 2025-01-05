import streamlit as st
from datetime import datetime
import Tools
from Estrattore import df

def run_heetmap():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    oggi = datetime.now().date()
    anno_corrente = oggi.year
    # permetto di scegliere un anno
    anno_selezionato = st.selectbox(
        "Seleziona un anno",
        [i for i in range(anno_corrente, anno_corrente - 11, -1)],
        index=0
    )
    Tools.stampa_heetmap(df,anno_selezionato)