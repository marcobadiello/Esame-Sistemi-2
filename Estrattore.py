import json
import polars as pl
import os
from datetime import datetime
import os
'''
In questo file viene gestita tutta la creazioen del datafarame dei dati.
I dati forniti da Spotify sono in formato Json e poichè sono tanto grandi
sono più file.
Le informzioen sulle varaibili presenti nel dataframe sono visibili sul pdf
"ReadMeFirst_ExtendedStreamingHistory.pdf"
'''

#questa funzione trasforma i file li pulisce e restituisce un dataframe
def data():
        # Percorso alla directory con i file
    directory = 'my_spotify_data/Spotify Extended Streaming History'
    # directory = 'my_spotify_data_ele/Spotify Extended Streaming History'
    # directory = 'my_spotify_data_milan/Spotify Extended Streaming History'

    # Lista per memorizzare i DataFrame
    dfs = []

    # Itera attraverso i file nella directory
    for filename in os.listdir(directory):
        # Percorso completo del file
        filepath = os.path.join(directory, filename)
        
        # Controlla che sia un file JSON
        if filename.endswith('.json'):
            with open(filepath, mode='r', encoding='utf-8') as file:
                # Leggi il JSON in un DataFrame
                df = pl.read_json(file, infer_schema_length=20000)
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
                dfs.append(df)

    # Concatena tutti i DataFrame
    if dfs:  # Assicurati che ci siano file JSON prima di concatenare
        df = pl.concat(dfs, how="vertical")
    else:
        print("Nessun file JSON trovato nella directory.")
    
    

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
# print(df['spotify_track_uri'])

''''
COSE IMPORTANTI DA SAPERE

- SI lo so per leggere i file si poteva fare un ciclo for ma non mi funzionava proprio bene quindi
ho deciso di fare così
- La variabile "df" che viene crate è una varibile globale che poi viene 
importare in praticamente tutti gli altri file
'''