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

def stampa_time_series(df):
      dataframe = anal.time_series(df)
      chart = (
            alt.Chart(dataframe).mark_line(point=True)
            .encode(
                  x = alt.X("periodo",title="Periodo"),
                  y = alt.Y("ore_riprodotte",title="Ore riprodotte")
            )
      )
      
      st.altair_chart(chart, use_container_width=True)
def stampa_time_series_cumulata(df):
      dataframe = anal.time_series_cumulata(df)
      chart = (
            alt.Chart(dataframe).mark_line(point = True)
            .encode(
                  x = alt.X("periodo",title="Periodo"),
                  y = alt.Y("ore_riprodotte_cumulate",title="Ore cumulate")
            )
      )
      st.altair_chart(chart, use_container_width=True)
def stampa_time_series_artisti(df, artisti: list, periodo):
    # Inizializza una lista per raccogliere i dataframe degli artisti
    dataframes = []

    # Ciclo su ogni artista e crea un dataframe per ciascuno
    for artista in artisti:
        # Ottieni i dati per l'artista corrente
        data = anal.time_series_artista(df, artista, periodo)

        # Aggiungi una colonna per il nome dell'artista
        data = data.with_columns(pl.lit(artista).alias("artista"))

        # Aggiungi il dataframe dell'artista alla lista
        dataframes.append(data)

    # Unisci tutti i dataframe in uno solo (concatenando verticalmente)
    df_completo = pl.concat(dataframes)

    # Palette di colori più contrastati
    colori_contrasti = [
        "#e41a1c", "#377eb8", "#4daf4a", "#ff7f00", "#ffff33", "#a65628", 
        "#f781bf", "#999999", "#f0027f", "#66c2a5"
    ]
    
    # Creiamo il grafico utilizzando Altair
    chart = (
        alt.Chart(df_completo.to_pandas())  # Converte il dataframe in pandas per Altair
        .mark_line(point=True)
        .encode(
            x=alt.X('periodo', title="Periodo"),  # Assumendo che 'periodo' sia di tipo DataTime
            y=alt.Y('ore_riprodotte:Q', title="Ore riprodotte"),
            color=alt.Color('artista:N', 
                            scale=alt.Scale(domain=artisti, range=colori_contrasti),
                            legend=alt.Legend(title="Artista"))
        )
    )

    # Visualizza il grafico in Streamlit
    st.altair_chart(chart, use_container_width=True)

    return df_completo