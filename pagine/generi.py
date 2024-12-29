from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

df1 = df
def run_generi():
    global df1
    df = df1
    Tools.stampa_generi(df,200)