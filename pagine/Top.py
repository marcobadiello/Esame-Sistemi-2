import Tools
import streamlit as st
def run_top():
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )

    Tools.stampa_top_n(n)