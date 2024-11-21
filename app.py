import streamlit as st
from Estrattore import df
import Tools
import polars as pl
import Analisi as anal

from pagine.Top import run_top
from pagine.home import run_home

pagine = {
    "Menù": [st.Page(run_home, title="Home", icon="🏠",default=True)],
    "": [st.Page(run_top, title="TOP", icon="🎖️")]
    
}
pg = st.navigation(pagine)
pg.run()



