from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st

def run_time_series():
    st.write(time_serie(df))