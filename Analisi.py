from Estrattore import df
import polars as pl
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import json
from pytube import Search, YouTube
from datetime import datetime, timedelta
import os
import streamlit as st


import icecream as ic

from credenziali import client_id
from credenziali import client_secret
from credenziali import redirect_uri

"""
Questo file contiene una serie di funzioni per l'analisi dei dati di ascolto musicale.
Le funzioni sono progettate per estrarre, filtrare e aggregare i dati in vari modi,
fornendo informazioni utili come le canzoni e gli artisti più ascoltati, le serie temporali
degli ascolti e altre statistiche rilevanti.
Funzioni principali:
- top_n_canzoni(df, n=None, periodo=None, artisti=None): Restituisce le canzoni più ascoltate
    in un determinato periodo, eventualmente filtrate per artista.
- top_n_artisti(df, n=None, periodo=None): Restituisce gli artisti più ascoltati in un determinato periodo.
- time_series_scorretto(df): Genera una serie temporale degli ascolti aggregati per anno e mese.
- dataframe_periodi(df): Crea un DataFrame con tutti i periodi (anno e mese) presenti nei dati.
- time_series(df): Corregge la serie temporale generata da time_series_scorretto aggiungendo i periodi con 0 ascolti.
- time_series_artista_scorretta(df, artista, periodo=None): Genera una serie temporale degli ascolti per un artista specifico.
- time_series_artista(df, artista, periodo=None): Corregge la serie temporale degli ascolti per un artista specifico.
- time_series_cumulata(df): Genera una serie temporale cumulata degli ascolti.
- shuffle_data(df): Restituisce statistiche sull'utilizzo della funzione 'shuffle'.
- media_oraria(df): Calcola la media degli ascolti per ogni ora del giorno.
- media_oraria_cumulata(df): Calcola la media cumulata degli ascolti per ogni ora del giorno.
- ascolto_generi(df, periodo, client_id, client_secret, redirect_uri): Restituisce una mappa dei generi musicali ascoltati in un determinato periodo.
- get_track_info(track_name): Restituisce informazioni su un brano specifico.
- get_profilo_info(): Restituisce informazioni sul profilo utente di Spotify.
- get_top_profilo(periodo, limit, offset=0): Restituisce le tracce e gli artisti più ascoltati dall'utente in un determinato periodo.
- search_youtube_video(video_name): Cerca un video su YouTube e restituisce l'URL del primo risultato.
- get_user_playlists(client_id, client_secret, redirect_uri): Restituisce le playlist dell'utente su Spotify.
- get_playlist_tracks(playlist_id, client_id, client_secret, redirect_uri): Restituisce le tracce di una playlist specifica su Spotify.
- crea_date_complete(anno): Crea un DataFrame con tutte le date di un anno specifico.
- ascolti_giornalieri(df, anno): Restituisce un DataFrame con gli ascolti giornalieri per un anno specifico.
"""


def top_n_canzoni(df,n=None,periodo=None,artisti=None):
    """
    Restituisce le canzoni più ascoltate in base ai parametri forniti.
    Args:
        df (DataFrame): Il DataFrame contenente i dati delle canzoni.
        n (int, optional): Il numero di canzoni da restituire. Se non specificato, restituisce tutte le canzoni.
        periodo (tuple, optional): Una tupla contenente due date (inizio, fine) per filtrare le canzoni in base al periodo.
        artisti (list, optional): Una lista di artisti per filtrare le canzoni in base agli artisti.
    Returns:
        DataFrame: Un DataFrame contenente le canzoni più ascoltate, ordinate in ordine decrescente di ascolti.
    """
    # se viene definito un periodo allora filtro in base a quel periodo altrimenti considero i
    # dati di sempre
    if periodo != None:
        new_df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1])) 
    if artisti != None:
        new_df = new_df.filter(pl.col("master_metadata_album_artist_name").is_in(artisti))
    # se imposto il parametro 'n' mi viene restituita la top n canzoni
    if n != None:
        return((new_df.group_by("master_metadata_track_name")
            .agg([pl.col("s_played").sum(),
                pl.col("spotify_track_uri").first(),
                pl.col("ts")])
            .sort("s_played",descending=True)
            .select("*")
            .head(n)
                ))
    # se il parametro 'n' non viene definito viene restituite tutte le 
    # canzoni del periodo in ordine decrescente
    
    else:
        return((new_df.group_by("master_metadata_track_name")
            .agg([pl.col("s_played").sum(),
                pl.col("spotify_track_uri").first(),
                pl.col("ts")])
            .sort("s_played",descending=True)
            .select("*")
                ))

def top_n_artisti(df,n=None,periodo=None):
    """
    Restituisce i migliori artisti in base al numero di riproduzioni (s_played) in un determinato periodo.

    Parameters:
    df (DataFrame): Il DataFrame contenente i dati delle riproduzioni.
    n (int, optional): Il numero di artisti da restituire. Se non specificato, restituisce tutti gli artisti.
    periodo (tuple, optional): Una tupla contenente due date (inizio, fine) per filtrare i dati in base al periodo. 
                               Se non specificato, considera tutti i dati.

    Returns:
    DataFrame: Un DataFrame contenente gli artisti e il numero totale di riproduzioni, ordinato in ordine decrescente.
               Se 'n' è specificato, restituisce solo i primi 'n' artisti.
    """
    
    # se viene selezionato un periodo filtro i dati in base a quel periodo
    if periodo != None:
        df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1]))
        
    # se imposto il parametro 'n' mi viene restituita la top n artisti
    if n != None:
        return((df.group_by("master_metadata_album_artist_name")
            .agg([pl.col("s_played").sum()])
            .sort("s_played",descending=True)
            .select("*")
            .head(n)
        ))
    
    # se il parametro 'n' non viene definito viene restituite tutte gli
    # artisti del periodo in ordine decrescente
    else:
        return((df.group_by("master_metadata_album_artist_name")
            .agg([pl.col("s_played").sum()])
            .sort("s_played",descending=True)
            .select("*")
        ))

def time_series_scorretto(df):
    """
    Elabora un DataFrame per estrarre anno e mese da una colonna di timestamp, 
    raggruppa i dati per anno e mese e calcola le ore totali riprodotte 
    per ciascun gruppo.
    Parametri:
    df (polars.DataFrame): Il DataFrame di input contenente una colonna 'ts' con 
                           timestamp e una colonna 's_played' con i secondi riprodotti.
    Restituisce:
    polars.DataFrame: Un DataFrame raggruppato per anno e mese con le ore totali 
                      riprodotte per ciascun gruppo.
    """
    # estraggo anno e mese dalle colonna ts
    df_new = df.with_columns(
        pl.col("ts").dt.year().alias("year"),
        pl.col("ts").dt.month().alias("month")
    )

    # ragruppo epr anno e mese sommo per i dati di ascolto
    grouped = df_new.group_by(["year", "month"]).agg(
        (pl.col("s_played").sum() / 3600).alias("total_hours_played")  # Converti i secondi in ore
    )
    
    # riordino i risultati per anno e mese
    grouped = grouped.sort(["year", "month"])
    
    return grouped

def dataframe_periodi(df):
    """
    Genera un DataFrame contenente i periodi (anno, mese) dal timestamp minimo al massimo nel DataFrame di input.
    Parametri:
    df (polars.DataFrame): DataFrame di input contenente una colonna 'ts' con dati di timestamp.
    Restituisce:
    polars.DataFrame: DataFrame con colonne 'anno' (anno), 'mese' (mese) e 'periodo' (numero sequenziale del periodo).
    """
    
    # estraggo il minimo e il amssimo dei peridoi dei miei dati
    periodo = (df['ts'].min(), df['ts'].max())
    
    # estraggo l'anno e il mese sia di inizio che di fine
    data_inizio, data_fine = periodo
    anno_iniziale = data_inizio.year
    mese_iniziale = data_inizio.month
    anno_finale = data_fine.year
    mese_finale = data_fine.month

    # genero una lsita di tuple (anno,mese)
    mesi = []
    anno, mese = anno_iniziale, mese_iniziale

    while (anno < anno_finale) or (anno == anno_finale and mese <= mese_finale):
        mesi.append((anno, mese))
        mese += 1
        if mese > 12:
            mese = 1
            anno += 1

    # creo il dataframe
    df_mesi = pl.DataFrame(mesi, schema=["anno", "mese"])

    # aggiungo la colonna periodo che aprte da uno e va avanti di 1 fino alla fine
    df_mesi = df_mesi.with_columns(
        pl.arange(1, len(df_mesi) + 1).alias("periodo")
    )
    
    return df_mesi

def time_series(df):
    """
    Genera un DataFrame di serie temporali con le ore totali riprodotte per ogni periodo.
    Parametri:
    df (DataFrame): Il DataFrame di input contenente i dati.
    Restituisce:
    DataFrame: Un DataFrame con le seguenti colonne:
        - 'anno': L'anno del periodo.
        - 'mese': Il mese del periodo.
        - 'ore_riprodotte': Le ore totali riprodotte per il periodo corrispondente.
        - 'data': Una stringa che combina 'anno' e 'mese' nel formato 'YYYY-MM'.
    """
    # creo i dataframe della time series e dei periodi di ascolto
    p = dataframe_periodi(df)
    d = time_series_scorretto(df)

    # creo le liste dei periodi
    lista_p = [f"{p['anno'][i]}-{p['mese'][i]}" for i in range(len(p))]
    lista_d = [f"{d['year'][i]}-{d['month'][i]}" for i in range(len(d))]

    # creo la lista delle ore riprodotte
    vere_ore = []
    thp = d["total_hours_played"].to_list()  # converto la colonna in una lista

    for periodo in lista_p:
        if periodo in lista_d:
            vere_ore.append(float(thp[lista_d.index(periodo)]))  # assicuro che il valore sia float
        else:
            vere_ore.append(0.0)  # se il periodo non è nella lista, aggiungo 0.0

    # aggiungi la colonna 'ore_riprodotte' con i valori corrispondenti a ogni riga
    df_finale = p.with_columns(
        pl.Series(name="ore_riprodotte", values=vere_ore)
    )

    # crea la colonna 'data' combinando 'anno' e 'mese'
    df_finale = df_finale.with_columns(
        (pl.col("anno").cast(pl.Utf8) + "-" + pl.col("mese").cast(pl.Utf8).str.zfill(2)).alias("data")
    )

    # crea una nuova colonna 'anno' estraendo solo l'anno dalla colonna 'data'
    df_finale = df_finale.with_columns(
        pl.col("data").str.slice(0, 4).alias("anno")
    )

    df_finale = df_finale.with_columns(
        df_finale["anno"].cast(pl.Int64)
    )




    return df_finale

def time_series_artista_scorretta(df, artista, periodo=None):
    """
    Genera una serie temporale delle ore totali riprodotte per un dato artista, eventualmente in un periodo specificato.
    Parametri:
    df (polars.DataFrame): Il DataFrame di input contenente i dati.
    artista (str): Il nome dell'artista da filtrare.
    periodo (tuple, opzionale): Una tupla contenente i timestamp di inizio e fine per filtrare i dati. Default è None.
    Restituisce:
    polars.DataFrame: Un DataFrame contenente le ore totali riprodotte per mese per l'artista specificato, 
                      eventualmente nel periodo specificato. Il DataFrame ha colonne 'year', 'month' 
                      e 'total_hours_played'.
    """
    
    # se viene selezinato un periodo filtro i dati in base a quel periodo
    if periodo is not None:
        df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <= periodo[1]))
    
    # filtro i dati in base all'artista che viene passato come parametro
    df = df.filter(pl.col("master_metadata_album_artist_name") == artista)
    
    # estraggo anno e mese dalla colonna 'ts'
    df = df.with_columns(
        pl.col("ts").dt.year().alias("year"),
        pl.col("ts").dt.month().alias("month")
    )
    
    # raggruppo per anno e mese e sommo i secondi di ascolto
    # per poi convertirli in ore e restituirli
    df_finale = (
        df.group_by(["year", "month"])  # Raggruppa per anno e mese
          .agg((pl.col("s_played").sum() / 3600).alias("total_hours_played"))  # Converti i secondi in ore
          .sort(["year", "month"])  # Ordina per anno e mese
    )
    



    return df_finale

def time_series_artista(df,artista,periodo=None):
    """
    Genera una serie temporale delle ore totali riprodotte per un dato artista nei periodi specificati.
    Parametri:
    df (DataFrame): Il DataFrame di input contenente i dati.
    artista (str): Il nome dell'artista da analizzare.
    periodo (str, opzionale): Il periodo da analizzare. Default è None.
    Restituisce:
    DataFrame: Un DataFrame con i periodi e le corrispondenti ore totali riprodotte per l'artista dato.
    Note:
    - La funzione crea due DataFrame: uno per i periodi e uno per le ore riprodotte.
    - Genera liste di periodi e ore riprodotte.
    - Garantisce che le ore riprodotte siano in formato floating-point.
    - Se l'artista non è presente in un dato periodo, assegna un valore di 0.0 per quel periodo.
    - Il DataFrame finale include una nuova colonna 'ore_riprodotte' con le ore totali riprodotte per ogni periodo.
    """
    
    # creo i dataframe dei periodi e delle ore di ascolto
    p = dataframe_periodi(df)
    d = time_series_artista_scorretta(df,artista)

    # creod delel liste di periodi
    lista_p = [f"{p["anno"][i]}-{p["mese"][i]}" for i in range(len(p))]
    lista_d = [f"{d["year"][i]}-{d["month"][i]}" for i in range(len(d))]

    # creo la lista delle ore riprodotte
    vere_ore = []
    # converto la colonna in una lista perchè faccio quello che mi pare
    thp = d["total_hours_played"].to_list()  
    for periodo in lista_p:
        if periodo in lista_d:
            # mi assicuro che il dato sia floating point
            vere_ore.append(float(thp[lista_d.index(periodo)]))  
        else:
            # se non c'è l'artista in quel mese/periodo assegno il valore 0.0
            vere_ore.append(0.0) 

    # aggiungo la colonna 'ore_riprodotte' con i valori corrispondenti a ogni riga
    df_finale = p.with_columns(
        pl.Series(name="ore_riprodotte", values=vere_ore)
    )

    return df_finale

def time_series_cumulata(df):
    """
    Genera una serie temporale cumulata dal DataFrame fornito.
    Questa funzione prende un DataFrame, estrae una serie temporale e aggiunge una colonna
    con la somma cumulata della colonna "ore_riprodotte". Successivamente rimuove
    le colonne non necessarie, lasciando solo "periodo", "ore_riprodotte_cumulate" 
    e "anno_int".
    Parametri:
    df (DataFrame): Il DataFrame di input contenente i dati della serie temporale.
    Restituisce:
    DataFrame: Un DataFrame con la serie temporale cumulata.
    """
    # Mi prendo la time series classica
    data = time_series(df)
    
    # Aggiungo la colonna con le ore cumulate
    data_cum = data.with_columns(
        (pl.col("ore_riprodotte").cum_sum()).alias("ore_riprodotte_cumulate")
    )

    # Cancello tutte le colonne che non mi servono in modo che mi resti solamente
    # la colonna "periodo", "ore_riprodotte_cumulate" e "anno_int"
    data_cum = data_cum.drop(["ore_riprodotte"])

    
    return data_cum

def shuffle_data(df):
    """
    Analizza la colonna 'shuffle' di un DataFrame e restituisce statistiche.

    Parametri:
    df (pandas.DataFrame): Il DataFrame contenente una colonna 'shuffle' con valori booleani.

    Restituisce:
    tuple: Una tupla contenente le seguenti statistiche:
        - Numero totale di voci (int)
        - Numero di valori True (int)
        - Numero di valori False (int)
        - Proporzione di valori True (float)
        - Proporzione di valori False (float)
    """
    l = df['shuffle'].to_list()
    tot = len(l)
    skip = 0 
    notskip = 0
    for i in l:
        if i == True:
            skip += 1
        else:
            notskip += 1
    risultati = (tot,skip,notskip,skip/tot,notskip/tot)
    return risultati

def media_oraria(df):
    """
    Calcola la distribuzione percentuale oraria delle osservazioni nel DataFrame fornito.

    Questa funzione prende un DataFrame con colonne 'ts' (timestamp) e 's_played' (osservazioni),
    e calcola la percentuale delle osservazioni totali per ogni ora del giorno (0-23).

    Args:
        df (pandas.DataFrame): Un DataFrame contenente le colonne 'ts' e 's_played'.

    Returns:
        polars.DataFrame: Un DataFrame con due colonne:
            - 'hour': L'ora del giorno (0-23).
            - 'observations': La percentuale delle osservazioni totali per ogni ora.
    """
    diz = {hour: 0 for hour in range(24)}
    for i in range(0,len(df)):
        ora = df['ts'][i].hour
        ascolto = df['s_played'][i]  
        diz[ora] = diz[ora] + ascolto
    totale = 0 
    for i in diz:
        totale = totale + diz[i]
    for i in diz:
        diz[i] = (diz[i]/totale)*100
    data = pl.DataFrame({
    "hour": list(diz.keys()),
    "observations": list(diz.values())
    })
    return data

def media_oraria_cumulata(df):
    """
    Calcola la media oraria cumulata delle osservazioni nel DataFrame fornito.
    Parametri:
    df (polars.DataFrame): Un DataFrame contenente i dati con osservazioni orarie.
    Restituisce:
    polars.DataFrame: Un DataFrame con due colonne:
        - 'hour': L'ora del giorno (0 a 23).
        - 'cum': La somma cumulata delle osservazioni fino a quell'ora.
    """
    data = media_oraria(df)
    
    ora = range(0,24)
    perc = []
    somma = 0
    for i in data['observations']:
        somma = somma + i
        perc.append(somma)
    df = pl.DataFrame({
    "hour": ora,
    "cum": perc
    })
    return df

def ascolto_generi(df,periodo,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri):
    """
    Analizza i generi musicali ascoltati dagli utenti in un determinato periodo.
    Args:
        df (DataFrame): Il dataframe contenente i dati degli ascolti.
        periodo (str): Il periodo di tempo per il quale analizzare gli ascolti.
        client_id (str): L'ID del client per l'autenticazione con Spotify.
        client_secret (str): Il segreto del client per l'autenticazione con Spotify.
        redirect_uri (str): L'URI di reindirizzamento per l'autenticazione con Spotify.
    Returns:
        dict: Un dizionario dove le chiavi sono i generi musicali e i valori sono il tempo totale di ascolto per ciascun genere.
    """
    startint = datetime.now()
    mappa = {}

    # Autenticazione con Spotify usando il OAuth Flow
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="user-library-read"))

    dataframe = top_n_artisti(df,periodo=periodo)
    # 1. Calcolare la somma totale di 's_played'
    total_played = dataframe["s_played"].sum()

    # 2. Aggiungere una colonna con la percentuale di ascolto per ogni artista
    dataframe = dataframe.with_columns(
        (pl.col("s_played") / total_played * 100).alias("percentage_of_total")
    )


    # 3. Filtrare gli artisti con una percentuale di ascolto superiore o uguale all'1%
    df_filtered = dataframe.filter(pl.col("percentage_of_total") >= 0.1)

    # Visualizzare il risultato

    for row in df_filtered.iter_rows():
        nome = row[0]
        tempo = row[1]


    # Cerca l'artista usando il nome
        results = sp.search(q='artist:' + nome, type='artist', limit=1)

    
     # Verifica se sono stati trovati risultati
        if results['artists']['items']:
            artist = results['artists']['items'][0]
            generi = artist['genres']
        else:
            pass

        for i in generi:
            if i not in mappa:
                mappa[i] = tempo
            else:
                mappa[i] += tempo

        

    return mappa

def get_track_info(track_name):
    """
    Recupera informazioni su un brano da Spotify.
    Args:
        track_name (str): Il nome del brano da cercare.
    Returns:
        dict: Un dizionario contenente i risultati della ricerca per il brano.
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="user-library-read"))
    # Ricerca del brano
    results = sp.search(q=track_name, type='track', limit=1)
    

    return results

def get_profilo_info():
    """
    Recupera le informazioni del profilo utente corrente da Spotify.
    Questa funzione utilizza la libreria Spotipy per autenticarsi con Spotify
    tramite OAuth e recupera le informazioni del profilo utente, inclusi dettagli
    privati e email.
    Returns:
        dict: Un dizionario contenente le informazioni del profilo utente.
    """
    scope = 'user-read-private user-read-email user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))
    

    # Ottenere informazioni sul profilo
    user_profile = sp.current_user()

    

    return user_profile

def get_top_profilo(periodo: str,limit: int,offset = 0):
    """
    Recupera le tracce e gli artisti più ascoltati dall'utente in un determinato periodo.
    Args:
        periodo (str): L'intervallo di tempo per gli elementi principali. I valori validi sono 'short_term' (4 settimane), 
                        'medium_term' (6 mesi) e 'long_term' (diversi anni).
        limit (int): Il numero di elementi da restituire. Il valore massimo è 50.
        offset (int, opzionale): L'indice del primo elemento da restituire. Il valore predefinito è 0.
    Returns:
        dict: Un dizionario contenente le tracce e gli artisti principali dell'utente con le chiavi 'top_track' e 'top_artist'.
    """
    scope = 'user-read-private user-read-email user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))
    


    user_top_track = sp.current_user_top_tracks(time_range=periodo,limit=limit,offset=offset)
    user_top_artist = sp.current_user_top_artists(time_range=periodo,limit=limit,offset=offset)
    
    risultati = {
        'top_track':user_top_track,
        'top_artist':user_top_artist
    }
    return risultati

def search_youtube_video(video_name):
    """
    Cerca un video su YouTube per nome e restituisce l'URL del primo risultato.

    Args:
        video_name (str): Il nome del video da cercare.

    Returns:
        str: L'URL del primo risultato video di YouTube se trovato, altrimenti None.

    Raises:
        Exception: Se si verifica un errore durante il processo di ricerca.
    """
    try:
        # Cerca il video su YouTube
        search = Search(video_name)
        video = search.results[0]  # Prende il primo risultato
        return video.watch_url
    except Exception as e:
        return None

def get_user_playlists(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri):
    """
    Recupera le playlist dell'utente da Spotify.
    Questa funzione utilizza la libreria Spotipy per autenticarsi con Spotify e recuperare le playlist dell'utente.
    Gestisce la paginazione per assicurarsi che tutte le playlist vengano recuperate.
    Args:
        client_id (str): L'ID client per l'applicazione Spotify.
        client_secret (str): Il client secret per l'applicazione Spotify.
        redirect_uri (str): L'URI di reindirizzamento per l'applicazione Spotify.
    Returns:
        dict: Un dizionario dove le chiavi sono gli indici delle playlist (a partire da 1) e i valori sono dizionari
              contenenti il nome della playlist, l'ID e l'URL della prima immagine (o un segnaposto se non è disponibile).
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-read-private"))
    
    offset = 0  # Inizializza l'offset
    risultati = {}
    while True:
        # Ottieni le playlist dell'utente con l'offset per la paginazione
        results = sp.current_user_playlists(offset=offset)
        playlists = results['items']
        
        # Aggiungi le playlist alla lista
        for idx, playlist in enumerate(playlists):
            name = playlist['name']
            playlist_id = playlist['id']
            images = playlist.get('images', [])
            
            # Controlla se ci sono immagini nella playlist
            if images:
                image_url = images[0]['url']  # Prendi la prima immagine
            else:
                image_url = "No image available"  # Se non ci sono immagini
            
            risultati[offset + idx + 1] = {
                'nome': name,
                'id': playlist_id,
                'foto': image_url
            }
        
        # Se il numero di playlist recuperate è inferiore a 50, significa che abbiamo raggiunto la fine
        if len(playlists) < 50:
            break
        
        # Altrimenti, incrementa l'offset di 50 per ottenere il blocco successivo
        offset += 50
    
    return risultati

def get_playlist_tracks(playlist_id, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri):
    """
    Recupera tutte le tracce da una playlist di Spotify.
    Args:
        playlist_id (str): L'ID Spotify della playlist.
        client_id (str): L'ID client per l'autenticazione API di Spotify.
        client_secret (str): Il client secret per l'autenticazione API di Spotify.
        redirect_uri (str): L'URI di reindirizzamento per l'autenticazione API di Spotify.
    Returns:
        dict: Un dizionario dove le chiavi sono gli indici delle tracce (a partire da 1) e i valori sono dizionari
              contenenti 'canzone' (nome della traccia) e 'artista' (nomi degli artisti).
    Example:
        >>> tracce = get_playlist_tracks('playlist_id', 'client_id', 'client_secret', 'redirect_uri')
        >>> print(tracce)
        {1: {'canzone': 'Nome Traccia 1', 'artista': 'Artista 1'},
         2: {'canzone': 'Nome Traccia 2', 'artista': 'Artista 2, Artista 3'},
         ...}
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-read-private"))
    offset = 0  # Inizializza l'offset
    risultati = {}  # Dizionario per memorizzare i risultati

    while True:
        # Ottieni le tracce della playlist con l'offset per la paginazione
        results = sp.playlist_tracks(playlist_id, offset=offset)
        tracks = results['items']
        
        # Aggiungi le tracce al dizionario
        for idx, item in enumerate(tracks):
            track = item['track']
            track_name = track['name']
            artists = ', '.join(artist['name'] for artist in track['artists'])  # Unisce i nomi degli artisti
            risultati[offset + idx + 1] = {
                'canzone': track_name,
                'artista': artists
            }
        
        # Se il numero di tracce recuperate è inferiore a 100, significa che abbiamo raggiunto la fine
        if len(tracks) < 100:
            break
        
        # Altrimenti, incrementa l'offset di 100 per ottenere il blocco successivo
        offset += 100

    return risultati

def crea_date_complete(anno):
    """
    Crea un DataFrame Polars contenente tutte le date di un anno specificato.
    Args:
        anno (int): L'anno per il quale creare l'elenco di date.
    Returns:
        pl.DataFrame: Un DataFrame Polars contenente tutte le date dell'anno specificato.
    Example:
        >>> crea_date_complete(2023)
        shape: (365, 1)
        ┌────────────┐
        │ giorno     │
        │ ---        │
        │ date       │
        ├────────────┤
        │ 2023-01-01 │
        │ 2023-01-02 │
        │ ...        │
        │ 2023-12-31 │
        └────────────┘
    """
    # Funzione per verificare se un anno è bisestile
    def is_bisestile(anno):
        return (anno % 4 == 0 and anno % 100 != 0) or (anno % 400 == 0)

    # Determinare il numero di giorni nell'anno
    giorni_nell_anno = 366 if is_bisestile(anno) else 365

    # Creare l'elenco di date
    date_list = []
    start_date = datetime(anno, 1, 1)

    for giorno in range(giorni_nell_anno):
        date_list.append((start_date + timedelta(days=giorno)).date())

    # Creare il DataFrame Polars
    date_complete = pl.DataFrame({"giorno": date_list})

    return date_complete

def ascolti_giornalieri(df, anno):
    """
    Calcola il totale del tempo di ascolto giornaliero per un determinato anno.
    Args:
        df (pl.DataFrame): Il DataFrame contenente i dati di ascolto con colonne "ts" (timestamp) e "s_played" (tempo di ascolto).
        anno (int): L'anno per il quale calcolare il totale del tempo di ascolto giornaliero.
    Returns:
        pl.DataFrame: Un DataFrame con due colonne: "data" (giorno) e "valore" (totale del tempo di ascolto per quel giorno).
                      Se un giorno non ha dati di ascolto, il valore sarà 0.
    """
    # Selezionare le colonne necessarie
    df_selezionato = df.select(["ts", "s_played"])
    print(df_selezionato)
    
    # Convertire il timestamp in formato giorno
    df = df.with_columns(
        pl.col("ts").dt.strftime("%Y-%m-%d").alias("giorno")
    )
    
    # Filtrare i giorni per l'anno indicato
    df = df.filter(pl.col("giorno").str.slice(0, 4) == str(anno))
    
    # Raggruppamento per giorno e somma del tempo di ascolto
    df_aggregated = df.group_by("giorno").agg(
        totale_ascolto=pl.col("s_played").sum()
    )
    
    # Creazione della lista di tutte le date dell'anno
    date_complete = crea_date_complete(anno)  # Assicurati che questa funzione esista e restituisca una lista di stringhe
    print(df_aggregated)
    print(date_complete)
    
    date_non_complete = {}
    for row in df_aggregated.iter_rows():
        date_non_complete[row[0]] = row[1]
        
    date_complete_lista = []
    for row in date_complete.iter_rows():
        date_complete_lista.append(row[0].strftime("%Y-%m-%d"))
        
    
    risultati = {}
    
    for i in date_complete_lista:
        if i in date_non_complete:
            risultati[i] = date_non_complete[i]
        else:
            risultati[i] = 0
    

   
    dataframe_finale = pl.DataFrame(list(risultati.items()), schema=["data", "valore"])

    return dataframe_finale
