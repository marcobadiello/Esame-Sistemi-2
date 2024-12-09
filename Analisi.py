from Estrattore import df
import polars as pl
from datetime import datetime
# def top(n=10,chiave="song",periodo=""):
    
def top_n_canzoni(df,n=None,periodo=None):
    if periodo != None:
        new_df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1]))
    if n != None:
        return((new_df.group_by("master_metadata_track_name")
            .agg([pl.col("s_played").sum(),
                pl.col("spotify_track_uri").first(),
                pl.col("ts")])
            .sort("s_played",descending=True)
            .select("*")
            .head(n)
                ))
    else:
        return((new_df.group_by("master_metadata_track_name")
            .agg([pl.col("s_played").sum(),
                pl.col("spotify_track_uri").first(),
                pl.col("ts")])
            .sort("s_played",descending=True)
            .select("*")
                ))

def top_n_artisti(df,n=None,periodo=None):
    if periodo != None:
        df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1]))
        
    if n != None:
        return((df.group_by("master_metadata_album_artist_name")
            .agg([pl.col("s_played").sum()])
            .sort("s_played",descending=True)
            .select("*")
            .head(n)
        ))
    else:
        return((df.group_by("master_metadata_album_artist_name")
            .agg([pl.col("s_played").sum()])
            .sort("s_played",descending=True)
            .select("*")
        ))
        

################### NON TOCCARE ASSOLUTAMETNE PER NESSUN MOTIVO QUESTE TRE FUNZIONI ##########################
def time_series_scorretto(df):
    # Estrai anno e mese dalla colonna 'ts'
    df_new = df.with_columns(
        pl.col("ts").dt.year().alias("year"),
        pl.col("ts").dt.month().alias("month")
    )

    # Raggruppa per anno e mese e somma i secondi di ascolto
    grouped = df_new.group_by(["year", "month"]).agg(
        (pl.col("s_played").sum() / 3600).alias("total_hours_played")  # Converti i secondi in ore
    )
    
    # Ordina i risultati per anno e mese
    grouped = grouped.sort(["year", "month"])
    
    # Aggiungi una colonna 'periodo' che parte da 1
    # grouped = grouped.with_columns(
    #     pl.arange(1, len(grouped) + 1).alias("periodo")  # Crea numeri sequenziali
    # )
    
    return grouped

def dataframe_periodi(df):
    # Estrai il periodo minimo e massimo
    periodo = (df['ts'].min(), df['ts'].max())
    # Estrai l'anno e il mese di inizio e fine
    data_inizio, data_fine = periodo
    anno_iniziale = data_inizio.year
    mese_iniziale = data_inizio.month
    anno_finale = data_fine.year
    mese_finale = data_fine.month

    # Genera una lista di tuple (anno, mese)
    mesi = []
    anno, mese = anno_iniziale, mese_iniziale

    while (anno < anno_finale) or (anno == anno_finale and mese <= mese_finale):
        mesi.append((anno, mese))
        mese += 1
        if mese > 12:
            mese = 1
            anno += 1

    # Crea il dataframe
    df_mesi = pl.DataFrame(mesi, schema=["anno", "mese"])

    # Aggiungi la colonna 'periodo' che parte da 1 e va avanti
    df_mesi = df_mesi.with_columns(
        pl.arange(1, len(df_mesi) + 1).alias("periodo")
    )
    
    return df_mesi
    
def time_series(df):
    # Crea i dataframe dei periodi e delle ore di ascolto
    p = dataframe_periodi(df)
    d = time_series_scorretto(df)

    # Creazione delle liste di periodi
    lista_p = [f"{p["anno"][i]}-{p["mese"][i]}" for i in range(len(p))]
    lista_d = [f"{d["year"][i]}-{d["month"][i]}" for i in range(len(d))]

    # Creazione della lista delle ore riprodotte
    vere_ore = []
    thp = d["total_hours_played"].to_list()  # Converto la colonna in lista per una gestione più semplice

    for periodo in lista_p:
        if periodo in lista_d:
            vere_ore.append(float(thp[lista_d.index(periodo)]))  # Assicurati che siano float
        else:
            vere_ore.append(0.0)  # Se non c'è l'artista in quel mese, assegno 0 come float

    # Aggiungi la colonna 'ore_riprodotte' con i valori corrispondenti a ogni riga
    df_finale = p.with_columns(
        pl.Series(name="ore_riprodotte", values=vere_ore)
    )

    return df_finale
#################################################################################################################




def time_series_artista_scorretta(df, artista, periodo=None):
    
    if periodo is not None:
        # Filtra i dati nel periodo specificato
        df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <= periodo[1]))
    
    # Filtra per l'artista specificato
    df = df.filter(pl.col("master_metadata_album_artist_name") == artista)
    
    # Estrai anno e mese dalla colonna 'ts'
    df = df.with_columns(
        pl.col("ts").dt.year().alias("year"),
        pl.col("ts").dt.month().alias("month")
    )
    
    # Raggruppa per anno e mese e somma i secondi di ascolto (convertiti in ore)
    return (
        df.group_by(["year", "month"])  # Raggruppa per anno e mese
          .agg((pl.col("s_played").sum() / 3600).alias("total_hours_played"))  # Converti i secondi in ore
          .sort(["year", "month"])  # Ordina per anno e mese
    )
    

def time_series_artista(df,artista,periodo=None):
    # Crea i dataframe dei periodi e delle ore di ascolto
    p = dataframe_periodi(df)
    d = time_series_artista_scorretta(df,artista)

    # Creazione delle liste di periodi
    lista_p = [f"{p["anno"][i]}-{p["mese"][i]}" for i in range(len(p))]
    lista_d = [f"{d["year"][i]}-{d["month"][i]}" for i in range(len(d))]

    # Creazione della lista delle ore riprodotte
    vere_ore = []
    thp = d["total_hours_played"].to_list()  # Converto la colonna in lista per una gestione più semplice

    for periodo in lista_p:
        if periodo in lista_d:
            vere_ore.append(float(thp[lista_d.index(periodo)]))  # Assicurati che siano float
        else:
            vere_ore.append(0.0)  # Se non c'è l'artista in quel mese, assegno 0 come float

    # Aggiungi la colonna 'ore_riprodotte' con i valori corrispondenti a ogni riga
    df_finale = p.with_columns(
        pl.Series(name="ore_riprodotte", values=vere_ore)
    )

    return df_finale

def time_series_cumulata(df):
    data = time_series(df)
    data_cum = data.with_columns(
    (pl.col("ore_riprodotte").cum_sum()).alias("ore_riprodotte_cumulate")
    )
    data_cum = data_cum.drop("anno")
    data_cum = data_cum.drop("mese")
    data_cum = data_cum.drop("ore_riprodotte")
    return data_cum

