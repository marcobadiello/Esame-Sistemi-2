import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df

def run_top_canzoni():
    oggi = datetime.now().date()
    anno_corrente = oggi.year
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")

    # Slider per il numero di canzoni
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )

    # Scelta del tipo di periodo
    opzione_periodo = st.radio(
        "Seleziona il periodo:",
        ["Dati di sempre", "Anno specifico", "Periodo personalizzato"]
    )

    # Gestione del periodo in base alla selezione
    if opzione_periodo == "Dati di sempre":
        # Usa l'intero range del DataFrame
        periodo = (df['ts'].min(), df['ts'].max())

    elif opzione_periodo == "Anno specifico":
        # Permetti di scegliere un anno
        anno_selezionato = st.selectbox(
            "Seleziona un anno",
            [i for i in range(anno_corrente, anno_corrente - 11, -1)],
            index=0
        )
        periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, 12, 31))

    elif opzione_periodo == "Periodo personalizzato":
        # Permetti di scegliere un intervallo di date
        start_date = st.date_input("Seleziona la data di inizio", value=datetime(anno_corrente, 1, 1).date())
        end_date = st.date_input("Seleziona la data di fine", value=oggi)
        if start_date > end_date:
            st.error("La data di inizio non può essere successiva alla data di fine.")
            return  # Esce dalla funzione se l'intervallo non è valido
        periodo = (start_date, end_date)

    # Visualizza il periodo selezionato e i risultati
    Tools.stampa_top_canzoni_n(df, n, periodo)
    st.write(f"Periodo selezionato: da {periodo[0].strftime('%Y-%m-%d')} a {periodo[1].strftime('%Y-%m-%d')}")

