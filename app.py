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
from pagine.generi import run_generi
from pagine.discover_artist import run_discover_artist
from pagine.discover_track import run_discover_track
from pagine.profilo import run_profilo
from pagine.readme import run_readme
from pagine.download_playlist import run_dawnload_playlist
from pagine.heetmap import run_heetmap



"""
Questo file è l'entry point dell'applicazione Streamlit. Importa vari moduli e funzioni necessari per il funzionamento dell'app,
inclusi i dati, strumenti e analisi. Inoltre, importa le funzioni che gestiscono le diverse pagine dell'applicazione.

Le pagine disponibili includono:
- Home
- Profilo
- Readme
- TOP Canzoni
- TOP Artisti
- Serie storica
- Serie storica artisti
- Shuffle
- Giornata tipo
- HeetMap
- Generi musicali
- Scopri artisti
- Scopri brani
- Dawnload playlist

Il dizionario 'pagine' contiene tutte le pagine del progetto, ognuna con il proprio titolo e icona.
L'applicazione avvia la navigazione tra queste pagine utilizzando Streamlit.
"""


# questo è un dizionario che contiene tutte le pagine del mio progetto
pagine = {
    "Menù": [st.Page(run_home, title="Home", icon="🏠",default=True)],
    "\t\t\t\t": [st.Page(run_profilo, title="Profilo", icon="🪪")],
    "\t\t\t\t\t": [st.Page(run_readme, title="Readme", icon="")],
    "TOP 🎖️": [st.Page(run_top_canzoni, title="TOP Canzoni", icon="")],
    "": [st.Page(run_top_artisti, title="TOP Artisti", icon="")],
    "Analisi": [st.Page(run_time_series, title="Serie storica", icon="")],
    "\n":[st.Page(run_time_series_artisti,title="Serie storica artisti")],
    "\n\n":[st.Page(run_shuffle,title="Shuffle?")],
    "\n\n\n":[st.Page(run_giornata,title="Giornata tipo")],
    "\n\n\n\t":[st.Page(run_heetmap,title="HeetMap")],
    "\n\n\n\n":[st.Page(run_generi,title="Generi musicali")],
    "Scopri": [st.Page(run_discover_artist, title="Scopri artisti", icon="")],
    "\t": [st.Page(run_discover_track, title="Scopri brani", icon="")],
    "\t\t\t": [st.Page(run_dawnload_playlist, title="Dawnload playlist", icon="")]
    
}

# avvio le pagine
pg = st.navigation(pagine)
pg.run()


