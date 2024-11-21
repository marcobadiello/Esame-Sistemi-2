import streamlit as st
from Estrattore import df

def run_home():
    st.title("Spotify wrapped statistico")
    st.write(df)