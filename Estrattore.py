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
    def trova_cartella_con_json(percorso_base):
        for root, dirs, files in os.walk(percorso_base):
            # Controlla se ci sono file JSON nella directory corrente
            for file in files:
                if file.endswith('.json'):
                    return root  # Restituisce la directory che contiene il file JSON
            # Se ci sono sottocartelle, esplora la successiva
            if dirs:  # dirs contiene sottocartelle
                sottocartella = os.path.join(root, dirs[0])
                return trova_cartella_con_json(sottocartella)
        return None  # Nessun file JSON trovato

    # Percorso di partenza
    percorso_base = 'DATI'

    # Cerca la cartella contenente il file JSON
    directory = trova_cartella_con_json(percorso_base)

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