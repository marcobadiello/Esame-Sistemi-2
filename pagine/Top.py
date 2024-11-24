import Tools
import streamlit as st
from datetime import datetime
from Estrattore import df
from Analisi import ultima_data

def run_top():
    # Data corrente
    oggi = datetime.now().date()

    # Calcola l'ultima data disponibile nei dati
    ultima_data = df['data'].max().date() if 'data' in df.columns else oggi

    # Selezione numero di canzoni
    n = st.slider(
        'Quante canzoni vuoi visualizzare?',
        min_value=1,
        max_value=100,
        value=3
    )

    # Opzione per visualizzare i dati di sempre
    dati_sempre = st.checkbox("Mostra dati di sempre (fino alla data più recente disponibile)")

    if dati_sempre:
        # Periodo impostato da una data generica fino all'ultima data disponibile
        periodo = (datetime(1970, 1, 1), ultima_data)
    else:
        # Selezione del periodo specifico
        anno_corrente = oggi.year
        mese_corrente = oggi.month
        giorno_corrente = oggi.day

        anno_selezionato = st.selectbox(
            "Seleziona un anno",
            [i for i in range(anno_corrente, anno_corrente - 11, -1)],
            index=0
        )

        # Imposta la fine dell'anno selezionato correttamente
        if anno_selezionato == anno_corrente:
            # Per l'anno corrente, usa il giorno attuale
            periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, mese_corrente, giorno_corrente))
        else:
            # Per anni passati, considera fino al 31 dicembre
            periodo = (datetime(anno_selezionato, 1, 1), datetime(anno_selezionato, 12, 31))

        # Gestione della selezione avanzata
        avanzato = st.checkbox("Selezione avanzata")
        if avanzato:
            start_date = st.date_input(
                "Seleziona la data di inizio",
                value=datetime(anno_selezionato, 1, 1)
            )
            end_date = st.date_input(
                "Seleziona la data di fine",
                value=datetime(anno_selezionato, 12, 31)
            )
            # Controllo validità intervallo date
            if start_date > end_date:
                st.error("La data di inizio deve essere precedente alla data di fine.")
            else:
                periodo = (start_date, end_date)

    # Visualizza il periodo selezionato
    st.write(f"Periodo selezionato: {periodo[0].strftime('%Y-%m-%d')} - {periodo[1].strftime('%Y-%m-%d')}")


    # Stampa i dati
    Tools.stampa_top_n(df, n, periodo)
