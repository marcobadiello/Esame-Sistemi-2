import json
import polars as pl
from datetime import datetime

'''
In questo file viene gestita tutta la creazioen del datafarame dei dati.
I dati forniti da Spotify sono in formato Json e poichè sono tanto grandi
sono più file.
Le informzioen sulle varaibili presenti nel dataframe sono visibili sul pdf
"ReadMeFirst_ExtendedStreamingHistory.pdf"
'''

#questa funzione trasforma i file li pulisce e restituisce un dataframe
def data(report=False):
    #converto il file json in una lisa python
    with open('my_spotify_data/data/json0.json', mode='r', encoding='utf-8') as file:
        df0 = pl.read_json(file,infer_schema_length=20000)
    with open('my_spotify_data/data/json1.json', mode='r', encoding='utf-8') as file:
        df1 = pl.read_json(file,infer_schema_length=20000)
    with open('my_spotify_data/data/json2.json', mode='r', encoding='utf-8') as file:
        df2 = pl.read_json(file,infer_schema_length=20000)
    with open('my_spotify_data/data/json3.json', mode='r', encoding='utf-8') as file:
        df3 = pl.read_json(file,infer_schema_length=20000)
    with open('my_spotify_data/data/json4.json', mode='r', encoding='utf-8') as file:
        df4 = pl.read_json(file,infer_schema_length=20000)
    df = pl.concat([df0, df1, df2, df3, df4], how="vertical")
    
    #il dataframe contiene molte informazioni non utili ai fini del progetto, 
    # procedo a rimuovere quelle che non mi interessano
    df = df.drop('platform')
    df = df.drop('conn_country')
    df = df.drop('ip_addr')
    df = df.drop('offline')
    df = df.drop('offline_timestamp')
    df = df.drop('incognito_mode')

    #rimuovo tutte le righe che riguardano i podcast
    df = df.filter(pl.col('episode_name').is_null())

    # ripulisco ulteriormente i podcast (forse questi codici non sono necessari) 
    # non ricordo sicneramente meglio non toccare nulla
    df = df.drop("episode_name")
    df = df.drop("episode_show_name")
    df = df.drop('spotify_episode_uri')

    # estraggo i codice identificativi delle canzoni
    df = df.with_columns(
        pl.col("spotify_track_uri").str.replace("spotify:track:","")
    )

    #converto i millisecondi in secondi perchè ha più senso
    df = df.with_columns(
        (pl.col('ms_played')/ 1000).alias('ms_played')
    )

    #rinomino la colonna da millisecondi a secondi 
    df = df.rename({'ms_played': 's_played'})

    #converto in oggetti datetime le date
    df = df.with_columns(pl.col("ts").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ"))

    return df

# creo il dataframe
df = data()


''''
COSE IMPORTANTI DA SAPERE

- SI lo so per leggere i file si poteva fare un ciclo for ma non mi funzionava proprio bene quindi
ho deciso di fare così
- La variabile "df" che viene crate è una varibile globale che poi viene 
importare in praticamente tutti gli altri file
'''