import streamlit as st
import Analisi as anal
import polars as pl
import Tools
from Estrattore import df
import altair as alt

def banner_canzone_small(codice):
    oo = f"""
    <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/track/{codice}?utm_source=generator" 
            width="100%" height="152" frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    st.markdown(oo, unsafe_allow_html=True)
def banner_canzone_big(codice):
    oo = f"""
    <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/track/{codice}?utm_source=generator" 
            width="100%" height="352" frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    st.markdown(oo, unsafe_allow_html=True)
def stampa_top_canzoni_n(df,n,periodo):
        data = anal.top_n_canzoni(df,n,periodo)
        total_sum = anal.top_n_canzoni(df,n=None,periodo=periodo)["s_played"].sum()
        st.subheader("Hai ascoltato un totale di ")
        st.subheader(convert_seconds(total_sum))

        for i in range(0,len(data)):
                numero = str(i+1)
                if numero == '1':
                      numero = numero + "🥇"
                elif numero == '2':
                      numero = numero + "🥈"
                elif numero == '3':
                      numero = numero + "🥉"
                print(numero)
                st.header(numero)
                st.subheader("Riprodotta per")
                st.subheader(convert_seconds(data.row(i)[1]))
                banner_canzone_small(data.row(i)[2])
                
def stampa_top_artisti(df,n,periodo):
      data = anal.top_n_artisti(df,n,periodo)

      for i in range(0,len(data)):
                numero = str(i+1)
                if numero == '1':
                      numero = numero + "🥇"
                elif numero == '2':
                      numero = numero + "🥈"
                elif numero == '3':
                      numero = numero + "🥉"
                print(numero)
                st.header(numero)
                st.title(f"{data.row(i)[0]}")
                st.subheader("Tempo di ascolto")
                st.subheader(convert_seconds(data.row(i)[1]))
                st.markdown("---")

def convert_seconds(seconds):
    days = seconds // 86400 
    seconds %= 86400
    hours = seconds // 3600 
    seconds %= 3600
    minutes = seconds // 60 
    seconds %= 60  
    return f"{round(days)} giorni, {round(hours)} ore, {round(minutes)} minuti, {round(seconds)} secondi"
def stampa_ts(df):
    # Assicurati che il DataFrame non sia lazy
    if isinstance(df, pl.LazyFrame):
        df = df.collect()  # Esegui il raccolto se è un LazyFrame
    
    # Creazione della colonna "anno-mese" con formato "YYYY-MM"
    df_new = df.with_columns(
        (pl.col("year").cast(str) + "-" + (pl.col("month").cast(str).str.zfill(2))).alias("year_month")
    )

    # Raggruppamento per anno-mese e calcolo dei secondi totali
    df_grouped = (
        df_new.group_by("year_month")
        .agg(pl.col("total_seconds_played").sum().alias("total_seconds"))
        .sort("year_month")
    )

    # Step 2: Creazione del grafico a linee con Altair
    st.title("Andamento degli ascolti mensili")
    st.write("Visualizzazione dinamica basata sul dataframe corrente")

    # Creazione del grafico usando direttamente i dati Polars
    chart = (
        alt.Chart(df_grouped.to_pandas())  # Convertiamo in Pandas solo per Altair
        .mark_line(color="blue", point=True)  # Linea con punti
        .encode(
            x=alt.X("year_month:O", title="Anno-Mese", axis=alt.Axis(labelAngle=-45)),  # Asse X con anno-mese
            y=alt.Y("total_seconds:Q", title="Secondi Totali"),
            tooltip=["year_month", "total_seconds"],
        )
        .properties(
            title="Secondi Totali Giocati per Mese",
            width=800,
            height=400,
        )
    ).configure_title(
        fontSize=18,
        anchor="middle",
    )

    # Step 3: Mostra il grafico in Streamlit
    st.altair_chart(chart, use_container_width=True)

    # Aggiungi una tabella interattiva con i dati aggregati
    st.write("Dati aggregati per anno e mese:")
    st.dataframe(df_grouped)