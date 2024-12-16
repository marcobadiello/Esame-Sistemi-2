from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

'''
In questo file c'è il codicce per la pagina streamlit realativa
ai dati riguardo l'utilizzo della modalità di shuffle
'''

def run_shuffle():
    Tools.stmapa_torta_shuffle(df)