import streamlit as st
from datetime import datetime
import Tools
from Estrattore import df

def run_heetmap():
    # Layout della pagina con colonne
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    
    # Data corrente e anno
    oggi = datetime.now().date()
    anno_corrente = oggi.year
    
    # Lista degli anni (ultimi 10 anni)
    lista_anni = [i for i in range(anno_corrente, anno_corrente - 11, -1)]
    
    # Trova l'indice dell'anno precedente
    indice_anno_precedente = lista_anni.index(anno_corrente - 1)
    
    # Selectbox per scegliere l'anno
    anno_selezionato = st.selectbox(
        "Seleziona un anno",
        lista_anni,
        index=indice_anno_precedente
    )
    
    # Richiamo della funzione per stampare la heatmap
    Tools.stampa_heetmap(df, anno_selezionato)