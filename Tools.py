import streamlit as st
import Analisi as anal
import polars as pl
import Tools
import polars as pl
import wikipedia
from Estrattore import df
import os
import pandas as pd
import yt_dlp
from pytube import YouTube
import altair as alt
from vega_datasets import data
import webbrowser
import math
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

from credenziali import client_id
from credenziali import client_secret
from credenziali import redirect_uri

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

def banner_artista_big(codice):
    # Crea il codice HTML per l'iframe utilizzando l'ID dell'artista
    oo = f"""
    <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/artist/{codice}?utm_source=generator" 
            width="100%" 
            height="352" 
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    # Mostra il banner in Streamlit
    st.markdown(oo, unsafe_allow_html=True)

def banner_artista_small(codice):
    # Crea il codice HTML per l'iframe utilizzando l'ID dell'artista
    oo = f"""
    <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/artist/{codice}?utm_source=generator" 
            width="100%" 
            height="152" 
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    # Mostra il banner in Streamlit
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
        if client_id and client_secret and redirect_uri != None:
            image_url = get_artist_image_url({data.row(i)[0]}, client_id=client_id, client_secret=client_secret)
        
        # Crea due colonne
        col1, col2 = st.columns([1, 3])  # La prima colonna è più stretta per l'immagine
        
        with col1:
            # Mostra l'immagine a sinistra
            if client_id and client_secret and redirect_uri != None:
                st.image(image_url, width=400)  # Puoi cambiare la larghezza dell'immagine se necessario
            else:
                st.error("Per visualizzare la foto dell'artista inserire le credenzili nel file credenziali.py")
        
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



# Funzione per visualizzare le informazioni di una traccia
def stampa_info_track(nome):
    global client_id
    global client_secret
    global redirect_uri
    # Recupera le informazioni della traccia
    data = anal.get_track_info(nome)['tracks']['items'][0]
    
    
    # Crea due colonne per visualizzare immagine album e nome traccia
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(data['album']['images'][0]['url'], width=400)
        if st.button("Scarica canzone"):
            Tools.download_audio_from_youtube(anal.search_youtube_video(f"{data['name']}{data['artists'][0]['name']}"))

    with col2:
        st.title(f"Titolo: {data['name']}")
        st.title(f"Artista: {data['artists'][0]['name']}")
        banner_canzone_small(data['id'])
    # Estrai i dati necessari
    album_nome = data['album']['name']
    album_release_date = data['album']['release_date']
    track_name = data['name']
    track_number = data['track_number']
    total_tracks = data['album']['total_tracks']
    popularity = data['popularity']  # Popolarità del brano (valore da 0 a 100)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="user-library-read"))
    results = sp.search(q='artist:' + data['artists'][0]['name'], type='artist', limit=1)

    
     # Verifica se sono stati trovati risultati
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        generi = artist['genres']
    else:
        pass
    

    # Verifica se è un singolo
    is_single = total_tracks == 1

    # Crea il testo informativo completo e mettilo in st.subheader
    if is_single:
        st.subheader(f"""
        Questo brano **{track_name}** è un singolo rilasciato il **{album_release_date}**.
        """)
        st.subheader(f"**I generi musicali che caratterizzano questo brano sono:**")
        if generi:
            for i in generi:
                st.subheader(f"➡️{i}")
        else:
            st.subheader("Nessun genere disponibile.")
                
                    
    else:
        st.subheader(f"""
        Dall'album '{album_nome}', pubblicato il **{album_release_date}**, il brano **{track_name}** si trova al numero **{track_number}** di **{total_tracks}** tracce.
        """)
        st.subheader(f"**I generi musicali che caratterizzano questo brano sono:**")
        if generi:
            for i in generi:
                st.subheader(f"➡️{i}")
        else:
            st.subheader("Nessun genere disponibile.")
                

        # Aggiungi il testo per il brano
    st.subheader(f"🔥 La popolarità di **{track_name}** è del **{popularity}%**!")

    # Codice HTML + CSS per creare la barra di progressione
    st.markdown(f"""
        <style>
        .progress-bar {{
            width: 100%;
            background-color: #e0e0e0;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .progress-bar > .bar {{
            height: 20px;
            width: {popularity}%;
            border-radius: 20px;
            background-color: {'#ff4d4d' if popularity < 50 else '#4caf50'};
            transition: width 0.5s ease;
        }}
        </style>
        <div class="progress-bar">
            <div class="bar"></div>
        </div>
    """, unsafe_allow_html=True)
    if popularity >= 70:
        st.header(f"Cosa ?!?! {popularity}% di popolarità 😱 Sembra che tu abbia trovato un capolavoro della musica! 🎉")
        st.balloons()
    
    st.video(anal.search_youtube_video(f"{data['name']}{data['artists'][0]['name']}"))

def stampa_info_artista(nome_artista):
    global client_id
    global client_secret
    global redirect_uri

    # Configura Spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read"
    ))

    # Cerca l'artista
    results = sp.search(q=f'artist:{nome_artista}', type='artist', limit=1)

    # Verifica se sono stati trovati risultati
    if not results['artists']['items']:
        st.error("Artista non trovato. Riprova con un altro nome.")
        return

    # Estrai i dettagli dell'artista
    artist = results['artists']['items'][0]
    artist_name = artist['name']
    artist_image = artist['images'][0]['url'] if artist['images'] else None
    generi = artist['genres']
    popularity = artist['popularity']  # Popolarità da 0 a 100
    followers = artist['followers']['total']
    artist_id = artist['id']
    spotify_link = artist['external_urls']['spotify']

    # Visualizza i dettagli dell'artista
    col1, col2 = st.columns([1, 3])

    with col1:
        if artist_image:
            st.image(artist_image, width=400)
            st.markdown(
            """
            <style>
            .stButton>button {
                background-color: #1DB954; /* Colore verde Spotify */
                color: black; /* Testo nero */
                font-size: 20px; /* Dimensioni del testo */
                padding: 20px 40px; /* Aumenta le dimensioni del bottone */
                border-radius: 10px; /* Angoli arrotondati */
                border: none;
                width: auto;
            }
            </style>
            """, unsafe_allow_html=True)

        # Bottone per aprire il profilo Spotify
        if st.button("Apri profilo Spotify"):
            webbrowser.open(spotify_link)

    with col2:
        st.title(f"{artist_name}")
        banner_artista_big(artist_id)
    
    len_followers = round((followers*1.6)/1000,2)
    st.subheader(f"👥 Numero di follower: {followers} se si tenessero tutti per mano sarebbero lunghi circa {len_followers} km ovvero {round(len_followers/40076,3) } volte il giro del mondo")
    
    st.subheader("I generi di questo artista sono:")
    if generi:
        for i in generi:
            st.subheader(f"➡️{i}")
    else:
        st.subheader("Nessun genere disponibile.")
        
    try:
        wikipedia.set_lang("it")
        # Ottieni il riassunto
        summary = wikipedia.summary(f"{artist_name} (gruppo musicale,cantante,musica)", sentences=5)
        # Mostra tutto il testo come un unico subheader
        st.markdown(f"{summary.split('=')[0]}")  # Livello 1 (più grande)
    except Exception as e:
        st.error(f"Scusa ma non ho trovato nulla rigurdo '{artist_name}'")
    
    st.warning(f"Queste informazione potrebbero non essere corrette o non riferirsi a '{artist_name}' per via i possibili errori di wikipedia")

    # Mostra la popolarità
    st.subheader(f"🔥 Popolarità: {popularity}%")

    # Barra di popolarità
    st.markdown(f"""
        <style>
        .progress-bar {{
            width: 100%;
            background-color: #e0e0e0;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .progress-bar > .bar {{
            height: 20px;
            width: {popularity}%;
            border-radius: 20px;
            background-color: {'#ff4d4d' if popularity < 50 else '#4caf50'};
            transition: width 0.5s ease;
        }}
        </style>
        <div class="progress-bar">
            <div class="bar"></div>
        </div>
    """, unsafe_allow_html=True)

    

    # Messaggio speciale per popolarità alta
    if popularity >= 70:
        st.header(f"Wow! {popularity}% di popolarità 😱! Questo artista è una divinità della musica! 🎉")
        st.balloons()

# periodo: str,limit: int,offset = 0
def stampa_profilo():
    user_data = anal.get_profilo_info()

    
    country = user_data['country']
    display_name = user_data['display_name']
    email = user_data['email']
    explicit_content_filter_enabled = user_data['explicit_content']['filter_enabled']
    explicit_content_filter_locked = user_data['explicit_content']['filter_locked']
    spotify_url = user_data['external_urls']['spotify']
    followers_total = user_data['followers']['total']
    profile_href = user_data['href']
    user_id = user_data['id']
    images = user_data['images']  # Lista delle immagini
    product = user_data['product']
    user_type = user_data['type']
    user_uri = user_data['uri']
    image_url = images[0]['url'] 
    
    st.title("🎵 Profilo Spotify")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_url, width=200)
    with col2:
        st.title(f"Ciao {display_name}")
    
    # Dividere in colonne
    col1, col2 = st.columns(2)

    # Colonna 1: Informazioni generali
    with col1:
        st.header("Informazioni generali")
        st.write(f"**Email:** {email}")
        st.write(f"**Paese:** {country}")
        st.write(f"**Tipo di account:** {product.capitalize()}")

    # Colonna 2: Contenuti espliciti e follower
    with col2:
        st.header("Dettagli aggiuntivi")
        st.write(f"**Contenuti espliciti abilitati:** {'Sì' if explicit_content_filter_enabled else 'No'}")
        st.write(f"**Contenuti espliciti bloccati:** {'Sì' if explicit_content_filter_locked else 'No'}")
        st.write(f"**Numero di follower:** {followers_total}")
    

    # Link e ID
    st.divider()
    st.subheader("Collegamenti utili")
    st.code(f"ID Utente: {user_id}", language="plaintext")
    st.code(f"URI Utente: {user_uri}", language="plaintext")
    if st.button("Apri profilo Spotify"):
        webbrowser.open(spotify_url)

def stampa_top_profilo(n,periodo):
    data = anal.get_top_profilo(periodo=periodo,limit=n)
    data_track = data['top_track']
    data_artisti = data['top_artist']
    risultati_track = {}
    risultati_artisti = {}
    posizione = 0
    for i in data_track['items']:
        posizione += 1
        nome = i['name']
        foto = i['album']['images'][0]['url']
        x = {
            'titolo':nome,
            'foto':foto
        }
        risultati_track[posizione] = x
        
    posizione = 0
    for i in data_artisti['items']:
        posizione += 1
        nome = i['name']
        foto = i['images'][0]['url']
        x = {
            'nome':nome,
            'foto':foto
        }
        risultati_artisti[posizione] = x
    col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
    with col1 and col2:
        st.subheader("Classsifica canzoni")
    with col3 and col4:
        st.subheader("Classifica artisti")
    
    for i in range(1,min(len(risultati_artisti),len(risultati_track))+1):

        
        col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
        with col1 and col2:
            st.divider()
        with col3 and col4:
            st.divider()
        with col1:
            st.image(f"{risultati_track[i]['foto']}", width=400)
        with col2:

            st.subheader(f"{i} - {risultati_track[i]['titolo']}")
        with col3:
            st.image(f"{risultati_artisti[i]['foto']}")
        with col4:
            st.subheader(f"{i} - {risultati_artisti[i]['nome']}")
    if n != min(len(risultati_artisti),len(risultati_track)):
        st.warning(f"Se non vedi esattamente {n} risultati è dovuto ad una mancanza di dati. Prova a ridurre il numero di risultati o ad aumentare la lunghezza del tuo periodo di intresse!")
    
def download_audio_from_youtube(url, output_path="DOWNLOAD"):
    try:
        # Crea la cartella di destinazione se non esiste
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Impostazioni per scaricare l'audio in formato MP3
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Cartella di salvataggio
            'format': 'bestaudio/best',  # Seleziona il miglior audio disponibile
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Usa FFmpeg per estrarre l'audio
                'preferredcodec': 'mp3',  # Converte in formato MP3
                'preferredquality': '192',  # Qualità dell'audio
            }],
            'ffmpeg_location': r'C:\path\to\ffmpeg\bin',  # Assicurati di avere ffmpeg installato e fornire il percorso
        }

        # Avvia il download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completato con successo!")

    except Exception as e:
        print(f"Errore durante il download: {e}")


def stampa_dawnload_palylist():
    # Ottieni le playlist
    playlist = anal.get_user_playlists()
    
    # Itera su ogni playlist
    for i in range(1, len(playlist) + 1):
        st.divider()
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # Mostra l'immagine della playlist con una dimensione ridotta
            st.image(playlist[i]['foto'], width=80)  # Modifica la larghezza per una foto più piccola
        
        with col2:
            # Mostra il nome della playlist in modo più grande
            st.subheader(f"{playlist[i]['nome']}", anchor=f"playlist_{i}")  # Aggiungi un anchor per una buona visibilità
        
        with col3:
            # Usa il nome della playlist come identificatore univoco per il bottone
            if st.button(f"Scarica {playlist[i]['nome']}"):
                st.write(f"Inizio il download...")
                id_playlist = playlist[i]['id']
                canzoni_nella_playlist = anal.get_playlist_tracks(id_playlist)
                for i in range(1,len(canzoni_nella_playlist)+1):
                    titolo = f"{canzoni_nella_playlist[i]['canzone']} {canzoni_nella_playlist[i]['artista']}"
                    try:
                        link = anal.search_youtube_video(titolo)
                    except:
                        link = None
                    if link:
                        download_audio_from_youtube(link)
                st.write(f"Download terminato")
                
def stampa_heetmap(df, anno):
    source = anal.ascolti_giornalieri(df, anno)

    # Estrai il giorno e il mese dalla colonna "data"
    source = source.with_columns([
        pl.col("data").str.slice(8, 2).alias("day"),  # Estrai il giorno
        pl.col("data").str.slice(5, 2).alias("month")  # Estrai il mese
    ])

    # Calcola il numero di ore di riproduzione (valore diviso per 3600)
    source = source.with_columns([
        (pl.col("valore") / 3600).alias("ore_riproduzione")  # Dividi per 3600 per ottenere ore
    ])

    # Crea la heatmap con Altair
    chart = alt.Chart(source.to_pandas(), title="Heatmap Giornaliera").mark_rect().encode(
        alt.X("day:O").title("Day").axis(labelAngle=0),
        alt.Y("month:O").title("Month"),
        alt.Color("ore_riproduzione:Q", scale=alt.Scale(scheme='viridis')).title("Ore di Riproduzione"),
        tooltip=[
            alt.Tooltip("data", title="Date"),
            alt.Tooltip("ore_riproduzione", title="Ore di Riproduzione"),
        ],
    ).configure_view(
        step=25,
        strokeWidth=0
    ).configure_axis(
        domain=False
    )

    # Visualizza la heatmap in Streamlit
    st.altair_chart(chart, use_container_width=True)
    
        
        
# ESTRAZIONE ARTISTI
