import json
import polars as pl
#creo una funzione che "pulisce" i miei dati
def data(report=False):
    #converto il file json in una lisa python
    with open('endsong_0.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
    df = pl.DataFrame(data)
    #il dataframe contiene molte informazioni non utili ai fini del progetto, procedo a rimuovere quelle che non mi interessano
    df = df.drop('username')
    df = df.drop('platform')
    df = df.drop('conn_country')
    df = df.drop('ip_addr_decrypted')
    df = df.drop('user_agent_decrypted')
    df = df.drop('offline')
    df = df.drop('offline_timestamp')
    df = df.drop('incognito_mode')
    #rimuovo i podcast
    df = df.filter(pl.col('episode_name').is_null())
    #rimuovo le colonne relative ai podcast
    df = df.drop("episode_name")
    df = df.drop("episode_show_name")
    df = df.drop('spotify_episode_uri')
    if report == True:
        print(df.columns)
        print(df)
    return df