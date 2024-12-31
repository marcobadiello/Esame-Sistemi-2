import streamlit as st
import Analisi as anal
import polars as pl
import Tools
from Estrattore import df
import os
import altair as alt
import math
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from credenziali import leggi_credenziali
cred = leggi_credenziali()
client_id = cred[0]
client_secret = cred[1]
redirect_uri = cred[2]
print(cred)

'''
In qesto file mi creo delle funzioni utili per allegerire poi il codice negli altri file
e renderlo più leggivile
'''

# questa funzione cra un banner piccole della canzone su streamlit
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
    
# questa funzione crea un banner grande di una canzone su streamlit
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

def get_artist_image_url(artist_name,client_id,client_secret):
    # Autenticazione con Spotify

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Cerca l'artista su Spotify
    result = sp.search(q=artist_name, type='artist', limit=1)
    
    # Se l'artista è trovato, restituisce il link della foto del profilo
    if result['artists']['items']:
        artist = result['artists']['items'][0]
        if artist['images']:
            return artist['images'][0]['url']
    return None  # Se l'artista non ha immagine o non è stato trovato

# questa funzione stampa la top 'n' delle canzoni
def stampa_top_canzoni_n(df,n,periodo):
      
      # ottengo il dataframe con la top
        numero_canzoni = anal.top_n_canzoni(df,n=None,periodo=periodo)['master_metadata_track_name'].n_unique() 
        data = anal.top_n_canzoni(df,n,periodo)
        total_sum = anal.top_n_canzoni(df,n=None,periodo=periodo)["s_played"].sum()
        
        # scrivo il tempo di ascolto
        st.subheader(f"Hai ascoltato {numero_canzoni} canzoni per un totale di ")
        st.subheader(convert_seconds(total_sum))
      # stampo le canzoni con una faccina per il podio
        for i in range(0,len(data)):
                st.markdown("---")
                numero = str(i+1)
                if numero == '1':
                      numero = numero + "🥇"
                elif numero == '2':
                      numero = numero + "🥈"
                elif numero == '3':
                      numero = numero + "🥉"
                st.header(numero)
                
                # scrivo il tempo di ascolto pe rla signola canzone
                st.subheader("Riprodotta per")
                st.subheader(convert_seconds(data.row(i)[1]))
                
                # stampo il banner con la canzone
                banner_canzone_small(data.row(i)[2])
  
# questa funzione stampa la top 'n' degli artisti
def stampa_top_artisti(df, n, periodo):
    # Ottengo la top artisti
    numero_artisti = anal.top_n_artisti(df, n=None, periodo=periodo)['master_metadata_album_artist_name'].n_unique() 
    data = anal.top_n_artisti(df, n, periodo)
    st.subheader(f"Hai ascoltato un totale di {numero_artisti} artisti ma i tuoi preferiti sono...")
    st.markdown("---")
    
    # Loop per mostrare gli artisti con l'immagine e le informazioni
    for i in range(0, len(data)):
        numero = str(i + 1)
        
        # Aggiungi emoji per il podio
        if numero == '1':
            numero = numero + "🥇"
        elif numero == '2':
            numero = numero + "🥈"
        elif numero == '3':
            numero = numero + "🥉"
        
        # Definisci qui l'URL dell'immagine (modifica questa variabile con il tuo URL)
        if os.path.exists("credenziali.txt"):
            image_url = get_artist_image_url({data.row(i)[0]}, client_id=client_id, client_secret=client_secret)
        else:
            errore = "Inserire credenziali per visualizzare foto"
        
        # Crea due colonne
        col1, col2 = st.columns([1, 3])  # La prima colonna è più stretta per l'immagine
        
        with col1:
            # Mostra l'immagine a sinistra
            if os.path.exists("credenziali.txt"):
                st.image(image_url, width=400)  # Puoi cambiare la larghezza dell'immagine se necessario
            else:
                st.error(errore)
        with col2:
            # Mostro l'artista e le informazioni nella colonna di destra
            st.header(numero)
            st.title(f"{data.row(i)[0]}")
            
            # Mostro il tempo di ascolto dell'artista specifico
            st.subheader("Tempo di ascolto")
            st.subheader(convert_seconds(data.row(i)[1]))
        
        st.markdown("---")



# questa funzione converte i secondi in giorni-ore-minuti-secondi
def convert_seconds(seconds):
    # è un codice molto semplice non penso di doverlo spiegare
    days = seconds // 86400 
    seconds %= 86400
    hours = seconds // 3600 
    seconds %= 3600
    minutes = seconds // 60 
    seconds %= 60  
    return f"{round(days)} giorni, {round(hours)} ore, {round(minutes)} minuti, {round(seconds)} secondi"

# questa funzione stampa un grafico di una time series
def stampa_time_series(df):
    # ottengo la time series
    dataframe = anal.time_series(df)

    # Crea il grafico
    chart = (
        alt.Chart(dataframe).mark_line(point=True)
        .encode(
            # sull'asse x metto il periodo ovvero ogni anno-mese
            x=alt.X('data:T', title='Periodo', 
                    axis=alt.Axis(labelAngle=-90)),  # etichette verticali
            # sull'asse y il tempo di ascolto in ore
            y=alt.Y('ore_riprodotte', title='Ore riprodotte'),
            # personalizza il tooltip per mostrare solo il mese e l'anno
            tooltip=[alt.Tooltip("anno",title='Anno'),
                     alt.Tooltip('mese:N', title='Mese'),
                     alt.Tooltip('ore_riprodotte', title='Ore riprodotte')]
        )
    )
    

    
    # stampo a schermo il grafico
    st.altair_chart(chart, use_container_width=True)

# questa funzione stampa il grafico di una time series cumulata
def stampa_time_series_cumulata(df):
      
      # ottengo la time series cumulata
      dataframe = anal.time_series_cumulata(df)
      
      # creo il grafico
      chart = (
        alt.Chart(dataframe).mark_line(point=True)
        .encode(
            # sull'asse x metto il periodo ovvero ogni anno-mese
            x=alt.X('data:T', title='Periodo', 
                    axis=alt.Axis(labelAngle=-90)),  # etichette verticali
            # sull'asse y il tempo di ascolto in ore
            y=alt.Y('ore_riprodotte_cumulate', title='Ore riprodotte'),
            # personalizza il tooltip per mostrare solo il mese e l'anno
            tooltip=[alt.Tooltip("anno",title='Anno'),
                     alt.Tooltip('mese:N', title='Mese'),
                     alt.Tooltip('ore_riprodotte_cumulate', title='Ore riprodotte')]
        )
    )
      
      # stampo il graficgrafico a schermo
      st.altair_chart(chart, use_container_width=True)

# questo grafico stampoa una time seriees dia rtisti a confronto
# il paramettro artisti che viene passato alla funzione infatti
# è una lista
def stampa_time_series_artisti(df, artisti: list, periodo):
    # inizializzo una lista per raccogliere i dataframe degli artisti
    dataframes = []

    # ciclo su ogni artista e crea un dataframe per ciascuno
    for artista in artisti:
          
        # ottengo i dati per l'artista corrente
        data = anal.time_series_artista(df, artista, periodo)

        # aggiungo una colonna per il nome dell'artista
        data = data.with_columns(pl.lit(artista).alias("artista"))

        # aggiungo il dataframe dell'artista alla lista
        dataframes.append(data)

    # unisco tutti i dataframe in uno solo (concatenando verticalmente)
    df_completo = pl.concat(dataframes)
    df_completo = df_completo.with_columns(
        (pl.col("anno").cast(pl.Utf8) + "-" + pl.col("mese").cast(pl.Utf8).str.zfill(2)).alias("data")
    )
    

    # creo una palette di colori più contrastati tanto permetto al massimo 10 confronti
    colori_contrasti = [
        "#e41a1c", "#377eb8", "#4daf4a", "#ff7f00", "#ffff33", "#a65628", 
        "#f781bf", "#999999", "#f0027f", "#66c2a5"
    ]
    
    # creo il grafico
    # non ho idea del perchè questo codice funzioni
    # NON TOCCARE NULLA
    print(df_completo)
    


    chart = (
          # Converte il dataframe in pandas per Altair
        alt.Chart(df_completo.to_pandas())  
        .mark_line(point=True)
        .encode(
            x=alt.X('data:T', title="Periodo",axis=alt.Axis(labelAngle=-90)),  
            y=alt.Y('ore_riprodotte:Q', title="Ore riprodotte"),
            tooltip=[alt.Tooltip("anno:N",title='Anno'),
                     alt.Tooltip('mese:N', title='Mese'),
                     alt.Tooltip('ore_riprodotte', title='Ore riprodotte')],
            

            color=alt.Color('artista:N', 
                            scale=alt.Scale(domain=artisti, range=colori_contrasti),
                            legend=alt.Legend(title="Artista"))
        )
    )

    # stampa il grafico a scehrmo
    st.altair_chart(chart, use_container_width=True)

    # mi restituisce anche il dataframe
    return df_completo

# questa funzione stampa un grafico per lo shuffle
def stmapa_torta_shuffle(df,colori):
    data = anal.shuffle_data(df)
    
    source = pl.DataFrame({
        "Opzioni": ["SHUFFLE ATTIVATO", "SHUFFLE DISATTIVATO"],
        "value": [round(data[3], 3), round(data[4], 3)]
    })

    chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta="value",
        color=alt.Color("Opzioni:N").scale(
            domain=["SHUFFLE ATTIVATO", "SHUFFLE DISATTIVATO"],
            range=[colori[0],colori[1]]  # Rosso per attivato, blu per disattivato
        )
    )
    
    st.altair_chart(chart, use_container_width=True)

# questa funzione stampa il grafico della giornata copiata da "https://altair-viz.github.io/gallery/polar_bar_chart.html"
def grafico_giornata(df,barra_evidenziata: int):
      data = anal.media_oraria(df)

      source = data


      polar_bars = alt.Chart(source).mark_arc(stroke='white', tooltip=True).encode(
      theta=alt.Theta("hour:O"),
      radius=alt.Radius('observations').scale(type='linear'),
      radius2=alt.datum(0),
      color = alt.condition(
            alt.datum.hour == barra_evidenziata,
            alt.value("red"),
            alt.value("steelblue")
          )
      )

      # Create the circular axis lines for the number of observations
      axis_rings = alt.Chart(pl.DataFrame({"ring": range(0, 11, 1)})).mark_arc(stroke='lightgrey', fill=None).encode(
      theta=alt.value(2 * math.pi),
      radius=alt.Radius('ring').stack(False)
      )
      axis_rings_labels = axis_rings.mark_text(color='grey', radiusOffset=5, align='left').encode(
      text="ring",
      theta=alt.value(math.pi / 4)
      )

      # Create the straight axis lines for the time of the day
      axis_lines = alt.Chart(pl.DataFrame({
      "radius": 10,
      "theta": math.pi / 2,
      'hour': ['00:00', '06:00', '12:00', '18:00']
      })).mark_arc(stroke='lightgrey', fill=None).encode(
      theta=alt.Theta('theta').stack(True),
      radius=alt.Radius('radius'),
      radius2=alt.datum(1),
      )
      axis_lines_labels = axis_lines.mark_text(
            color='grey',
            radiusOffset=5,
            thetaOffset=-math.pi / 4,
            # These adjustments could be left out with a larger radius offset, but they make the label positioning a bit clearner
            align=alt.expr('datum.hour == "18:00" ? "right" : datum.hour == "06:00" ? "left" : "center"'),
            baseline=alt.expr('datum.hour == "00:00" ? "bottom" : datum.hour == "12:00" ? "top" : "middle"'),
      ).encode(text="hour")
      
      lancetta = alt.Chart(pl.DataFrame({
        'theta': [barra_evidenziata * (360 / 24)],  # Calcola l'angolo in base all'ora
        'radius': [15],  # Lunghezza della lancetta
        })).mark_line(color='green', strokeWidth=7).encode(
        theta=alt.Theta("theta:Q", scale=alt.Scale(domain=[0, 360])),
        radius=alt.Radius("radius:Q", scale=alt.Scale(domain=[0, 10]))
        )

      chart = alt.layer(
      axis_rings,
      axis_rings_labels,
      axis_lines_labels,
      axis_lines,
      polar_bars,
      lancetta
      ).properties(
    width=800,  # Aumenta larghezza
    height=800 # Aumenta altezza
      )

      st.altair_chart(chart, use_container_width=True)

def grafico_giornata_orizzontale(df, n: int):
    data = anal.media_oraria(df)  # Non modifico i dati di partenza
    
    source = data

    # Grafico principale ad area
    area_chart = alt.Chart(source).mark_area(
        line={'color': 'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='darkgreen', offset=1)
            ],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        alt.X('hour:O', title='Ora del giorno'),  # Usa "hour" come variabile categorica
        alt.Y('observations:Q', title='Percentuale')  # Variabile numerica
    )

    # Linea verticale sottile rossa
    line_chart = alt.Chart(pl.DataFrame({'hour': [n]})).mark_rule(
        color='red',
        strokeWidth=2  # Linea sottile
    ).encode(
        x=alt.X('hour:O')  # Usa la stessa scala dell'asse X
    )

    # Layer combinato
    chart = area_chart + line_chart

    # Visualizza il grafico con Streamlit
    st.altair_chart(chart, use_container_width=True)

def grafico_giornata_orizzontale_cumulato(df, n: int):
    data = anal.media_oraria_cumulata(df)  # Non modifico i dati di partenza
    
    source = data

    # Grafico principale ad area
    area_chart = alt.Chart(source).mark_area(
        line={'color': 'darkred'},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='darkred', offset=1)
            ],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        alt.X('hour:O', title='Ora del giorno'),  # Usa "hour" come variabile categorica
        alt.Y('cum:Q', title='Percentuale')  # Variabile numerica
    )

    # Linea verticale sottile rossa
    line_chart = alt.Chart(pl.DataFrame({'hour': [n]})).mark_rule(
        color='red',
        strokeWidth=2  # Linea sottile
    ).encode(
        x=alt.X('hour:O')  # Usa la stessa scala dell'asse X
    )

    # Layer combinato
    chart = area_chart + line_chart

    # Visualizza il grafico con Streamlit
    st.altair_chart(chart, use_container_width=True)

def stampa_generi(df, n, periodo):
    # Ottenere i dati di ascolto (salvato nella cache)
    data = anal.ascolto_generi(df,periodo=periodo)

    # Calcolare il totale delle ore di ascolto
    total_listening_time = sum(data.values())

    # Convertire il dizionario in un DataFrame di Polars
    df_pl = pl.DataFrame(list(data.items()), schema=['Genre', 'Listening Time'])

    # Convertire il DataFrame di Polars in un DataFrame pandas per Altair
    df = df_pl.to_pandas()

    # Calcolare la percentuale di ascolto per ogni genere
    df['Percentage'] = round((df['Listening Time'] / total_listening_time) * 100, 2)

    # Ordinare i generi per la percentuale di ascolto (dal più ascoltato al meno ascoltato)
    df = df.sort_values(by='Percentage', ascending=False)

    # Limitare il DataFrame ai primi n generi
    df = df.head(n)

    # Creare il grafico con Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Percentage:Q', title='Percentuale di Ascolto (%)'),
        y=alt.Y('Genre:N', sort='-x', title='Genere Musicale'),
        color=alt.Color('Genre:N', legend=None),  # Usa colori ad alta distinzione
        tooltip=['Genre:N', 'Percentage:Q']
    ).properties(
        title=f"Distribuzione della Percentuale di Ascolto per i Primi {n} Generi Musicali"
    )

    # Visualizzare il grafico con Streamlit
    st.title(f'Distribuzione della Percentuale di Ascolto per i Primi {n} Generi Musicali')
    st.altair_chart(chart, use_container_width=True)

