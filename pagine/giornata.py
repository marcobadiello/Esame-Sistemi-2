from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

'''
In questo file c'è il codice per descrivere gli ascolti durante la gironatata
'''

def run_giornata():
    st.write("Giornata")
    orario_selezionato = st.slider(
        label="Seleziona orario",
        min_value=0,
        max_value=23,
        value=None
    )
    Tools.grafico_giornata(df,orario_selezionato)
    
