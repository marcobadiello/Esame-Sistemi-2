import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df



def run_top():
    oggi = datetime.now().date()
    anno = oggi.year
    mese = oggi.month
    giorno = oggi.day
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )
    periodo = (datetime(anno,1,1),datetime(anno,mese,giorno))
    anno_selezionato = st.selectbox("Seleziona un anno",[i for i in range(anno,anno-11,-1)],index=0)
    if st.button("Seleziona"):
        x = 1
    if st.button("Selezione avanzata"):
        start_date = st.date_input("Seleziona la data di inizio", value=datetime(anno_selezionato, 1, 1))
        end_date = st.date_input("Seleziona la data di fine", value=datetime(anno_selezionato, 12, 31))
        periodo = (start_date,end_date)




    

    Tools.stampa_top_n(df,n,periodo)
    print(periodo)