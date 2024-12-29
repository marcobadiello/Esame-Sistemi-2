from Estrattore import df
import polars as pl
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import json


import icecream as ic

'''
In questo file vengono definite tutte le funzioni che hanno come
scopo un analisi dei dati pecifica e restituiscono i dati richiesti
'''
client_id = '0c495503d007492cb9ab221bc097e13c'
client_secret = 'd03ba7bbe9f749d0b47bea40a0f11882'
redirect_uri = 'http://localhost:8888/callback'
# definisco una funzione per restituire la top delle canzoni di una determianto peridoo
def top_n_canzoni(df,n=None,periodo=None):
    
    # se viene definito un periodo allora filtro in base a quel periodo altrimenti considero i
    # dati di sempre
    if periodo != None:
        new_df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1])) 
        
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
        
# definisco una funzione per restituire la top degli artisti di un determinato periodo
def top_n_artisti(df,n=None,periodo=None):
    
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
        
################### NON TOCCARE ASSOLUTAMETNE PER NESSUN MOTIVO QUESTE TRE FUNZIONI ##########################

# questa funzione mi restiruisce una time series che però viene perfezionata da una funzine dopo
#
#il problema di questa funzione e che non restituisce un periodo se durante quel periodo non ci sono ascolti
#quindi la funzione che corregge questa funzione ha il compito di aggiungere i periodo con 0 ascolti
#
def time_series_scorretto(df):
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

# questa funzione prende tutti i mesi dei dati e ci associa un peridoo
def dataframe_periodi(df):
    
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

# questa funzioen ha il compito di correggere la time series restituita dalla prima funzione di queste 
# tre funzioni che NON VANNO TOCCATE 
def time_series(df):
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
#################################################################################################################

# questa funzione mi serve per restituirmi una time series filtrata per un artista
# 
# questa funzione spudoratamente copiata dalla funzione precedente ha il suo sesso problema ovvero non
# riesce a gestire il caso in cui in periodo non viene ascoltato l'artista
# per cu anche per questo caso è necessario che l'output di questa funzione venga corretto dalla
# funzione successiva
#
def time_series_artista_scorretta(df, artista, periodo=None):
    
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
    

    print(df_finale)

    return df_finale
# questa funzine ha il compito di correggere la funzione precedente come nel caso di prima 
# viene sfrittata la funzione dataframe_periodi(df) per avere un dataframe completo dei periodi
def time_series_artista(df,artista,periodo=None):
    
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

# quezt funzione mi restituisce un dataframe con la time series cumulata
# ovvero ad ogni periodo viene indicato il numero di ore riprodotto dall'inizio fino a quel periodo
def time_series_cumulata(df):
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


# questa funzione mi restituisce una tubla con tutte le informazioni in merito
# all'utilizzo della funzione 'shuffle'
def shuffle_data(df):
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

# questa funzione mi restituisci gli ascolti medi divisi per ora
def media_oraria(df):
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

def ascolto_generi(df,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri):
    startint = datetime.now()
    diz = {}
    new_col = []

    # Autenticazione con Spotify usando il OAuth Flow
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="user-library-read"))
    print(df)
    dataframe = df.select(['master_metadata_album_artist_name','spotify_track_uri','s_played'])
    print(dataframe)
    for row in dataframe.iter_rows():
        nome_artista = row[0]
        code = row[1]
        if nome_artista not in diz:
            search_result = sp.search(q=nome_artista, type='artist', limit=1)
            if search_result['artists']['items']:
                # Ottieni le informazioni dell'artista
                artist_info = search_result['artists']['items'][0]
                genres = artist_info.get('genres', [])
            else:
                genres = None
            diz[nome_artista] = genres
            print(nome_artista,'---',genres)
            new_col.append(genres)
        else:
            new_col.append(diz[nome_artista])
    dataframe = dataframe.with_columns(
        pl.Series(name="generi", values=new_col)
    )
    print(dataframe)
    dataframe.write_json("dataframe_con_generi.json")

    
    
    stopint = datetime.now()
    print("Tempo ricavo generi -> ",stopint-startint)

    conclusioni = {}
    for row in dataframe:
        generi = row[3]
        tempo = row[2]
        if generi:
            for i in generi:
                if i not in conclusioni:
                    conclusioni[i] = 0.0
                conclusioni[i] = conclusioni[i] + tempo
    nome_file = "generi.json"

    # Salvare il dizionario come JSON nel file
    with open(nome_file, "w", encoding="utf-8") as file:
        json.dump(conclusioni, file, ensure_ascii=False, indent=4)

    print(f"Dizionario salvato come JSON nel file '{nome_file}'.")

def aaa():
        # Specifica il percorso del file JSON
    file_path = "dataframe_con_generi.json"

    # Legge il file JSON
    with open(file_path, "r",encoding="utf-8") as f:
        data = json.load(f)

    mappa = {}


    for elemento in data:
        generi = elemento['generi']
        tempo = elemento['s_played']
        for i in generi:
            if i not in mappa:
                mappa[i] = tempo
            else:
                mappa[i] += tempo
    mappa = dict(sorted(mappa.items(), key=lambda item: item[1], reverse=False))
    for i in mappa:
        print(f"{i} -> {mappa[i]}")



    


start = datetime.now()
# ascolto_generi(df)
stop = datetime.now()
print("Tempo totale -> ",stop-start)
aaa()
'''
COSE IMPORTANTI DA SAPERE
- Ogni periodo corrisponde ad un mese quindi ogni 12 periodi corrisponde un anno
'''




#########################################

