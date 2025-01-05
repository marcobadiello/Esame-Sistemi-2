from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

from credenziali import client_id
from credenziali import client_secret
from credenziali import redirect_uri

df1 = df
def run_generi():
    global df1
    df = df1
    
    if client_id and client_secret and redirect_uri != None:
        st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )


        oggi = datetime.now().date()
        anno_corrente = oggi.year
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("spotify_logo.png", width=100)
        with col2:
            st.title("Spotify Wrapped Statistico")

        # scelta del tipo di periodo
        opzione_periodo = st.radio(
            "Seleziona il periodo:",
            ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
        )

        # gestisco il periodo in base alla selezione
        if opzione_periodo == "Dati di sempre":
            # utilizza l'intero range del dataframe
            periodo = (df['ts'].min(), df['ts'].max())

        elif opzione_periodo == "Anno specifico":
            # permetto di scegliere un anno
            anno_selezionato = st.selectbox(
                "Seleziona un anno",
                [i for i in range(anno_corrente, anno_corrente - 11, -1)],
                index=0
            )
            periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, 12, 31))

        elif opzione_periodo == "Periodo personalizzato":
            # permetto di scegliere un intervallo di date
            start_date = st.date_input("Seleziona la data di inizio", value=datetime(anno_corrente, 1, 1).date())
            end_date = st.date_input("Seleziona la data di fine", value=oggi)
            if start_date > end_date:
                st.error("La data di inizio non può essere successiva alla data di fine.")
                return  # esce dalla funzione se l'intervallo non è valido
            periodo = (start_date, end_date)
        n = st.slider("Quanti generi vuoi visualizzare?",min_value=1,max_value=50,value=10)
        xx = '''
        In questo grafico è possibile vedere le percentuali dei generi musicali ascoltati in un determinato periodo di tempo. 
        Notare che i dati vengono clacolati solo in base agli artisti che hannno un ascolto complessivo superiore al 0.1% nel peridoo di tempo 
        selezionato.
        '''
        st.write(xx)
        st.warning("La generazione del grafcio potrebbe richiedere qualche secondo in più")
        Tools.stampa_generi(df,n,periodo=periodo)
    else:
        st.warning("Attenzione per utilizzare questa pagina inserire le credenziali nel file credenziali.py")