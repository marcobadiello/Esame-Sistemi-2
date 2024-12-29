from Estrattore import df
from Analisi import time_series
import polars as pl
import altair as alt
import streamlit as st
import Tools
from datetime import datetime
import Analisi as anal

def run_generi():
    # Ottenere i dati di ascolto (salvato nella cache)
    data = anal.ascolto_generi(df)

    # Calcolare il totale delle ore di ascolto
    total_listening_time = sum(data.values())

    # Convertire il dizionario in un DataFrame di Polars
    df_pl = pl.DataFrame(list(data.items()), schema=['Genre', 'Listening Time'])

    # Convertire il DataFrame di Polars in un DataFrame pandas per Altair
    df = df_pl.to_pandas()

    # Calcolare la percentuale di ascolto per ogni genere
    df['Percentage'] = (df['Listening Time'] / total_listening_time) * 100

    # Ordinare i generi per la percentuale di ascolto (dal più ascoltato al meno ascoltato)
    df = df.sort_values(by='Percentage', ascending=False)

    # Creare il grafico con Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Percentage:Q', title='Percentuale di Ascolto (%)'),
        y=alt.Y('Genre:N', sort='-x', title='Genere Musicale'),
        color='Genre:N',
        tooltip=['Genre:N', 'Percentage:Q']
    ).properties(
        title="Distribuzione della Percentuale di Ascolto per Genere Musicale"
    )

    # Visualizzare il grafico con Streamlit
    st.title('Distribuzione della Percentuale di Ascolto per Genere Musicale')
    st.altair_chart(chart, use_container_width=True)