import streamlit as st
from Estrattore import df
import Tools
import polars as pl
import Analisi as anal

import Operazioni_preliminary

from pagine.Top_canzoni import run_top_canzoni
from pagine.home import run_home
from pagine.Top_artisti import run_top_artisti
from pagine.time_series import run_time_series

Operazioni_preliminary.start()


pagine = {
    "Menù": [st.Page(run_home, title="Home", icon="🏠",default=True)],
    "TOP 🎖️": [st.Page(run_top_canzoni, title="TOP Canzoni", icon="")],
    "": [st.Page(run_top_artisti, title="TOP Artisti", icon="")],
    "Analisi": [st.Page(run_time_series, title="Time Series", icon="")]
    
}
pg = st.navigation(pagine)
pg.run()



