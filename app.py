import streamlit as st
from Estrattore import df
import Tools
import polars as pl
import Analisi as anal


from pagine.Top_canzoni import run_top_canzoni
from pagine.home import run_home
from pagine.Top_artisti import run_top_artisti
from pagine.time_series import run_time_series
from pagine.time_series_artisti import run_time_series_artisti
from pagine.shuffle import run_shuffle
from pagine.giornata import run_giornata



#Questo file rappresentaa il "main" di tutto il progetto.
#Qui vengono gestite tutte e pagine e il loro relativo caricamento.


# questo è un dizionario che contiene tutte le pagine del mio progetto
pagine = {
    "Menù": [st.Page(run_home, title="Home", icon="🏠",default=True)],
    "TOP 🎖️": [st.Page(run_top_canzoni, title="TOP Canzoni", icon="")],
    "": [st.Page(run_top_artisti, title="TOP Artisti", icon="")],
    "Analisi": [st.Page(run_time_series, title="Serie storica", icon="")],
    "\n":[st.Page(run_time_series_artisti,title="Serie storica artisti")],
    "\n\n":[st.Page(run_shuffle,title="Shuffle?")],
    "\n\n\n":[st.Page(run_giornata,title="Giornata tipo")]
    
}

# avvio le pagine
pg = st.navigation(pagine)
pg.run()





#COSE IMPORTANTI DA SAPERE
#- Il file di ogni pagine è scritto interamente all'interno di una funzione la 
#quale viene importata nel secondo blocco di importazioni
#- Per avviare il progetto aprire il terminale e lanciare il comando "uv run stremalit run app.py"
#in alternativa il progetto potrebbe essere online al link "progettodimarco.streamlit.app"



