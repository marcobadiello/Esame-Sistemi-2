import streamlit as st
import Analisi as anal
import Tools
from Estrattore import df

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
