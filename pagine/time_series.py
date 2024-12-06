from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
import Analisi as anal

def run_time_series():
    dataframe = anal.time_series(df)


    chart = (
        alt.Chart(dataframe).mark_line(point=True)
        .encode(
            x = alt.X("periodo"),
            y = alt.Y("total_seconds_played")
        )
    )
    
    st.altair_chart(chart, use_container_width=True)
