import streamlit as st
from Estrattore import df

def run_home():
    st.title("Spotify wrapped statistico")
    if st.button("Mostra dataframe"):
        st.write(df)