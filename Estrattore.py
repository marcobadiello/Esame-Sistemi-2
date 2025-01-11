import json
import polars as pl
import os
from datetime import datetime
import os
"""
Questo script gestisce la creazione e la trasformazione di un DataFrame a partire dai dati forniti da Spotify in formato JSON.
I dati sono distribuiti su più file a causa delle loro dimensioni. Lo script cerca automaticamente i file JSON in una directory di base,
li legge, pulisce e concatena in un unico DataFrame. Le informazioni sulle variabili presenti nel DataFrame sono disponibili nel documento
"ReadMeFirst_ExtendedStreamingHistory.pdf".
"""

def data():
    """
    Cerca una cartella contenente file JSON a partire da una directory base, legge i file JSON trovati,
    li converte in DataFrame, rimuove colonne e righe non necessarie, concatena i DataFrame risultanti,
    e applica alcune trasformazioni sui dati.
    Returns:
        pl.DataFrame: Un DataFrame contenente i dati trasformati dai file JSON trovati.
    """
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