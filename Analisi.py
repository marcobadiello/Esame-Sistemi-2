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

def top_n_artisti(df,n,periodo=None):
    if periodo != None:
        df = df.filter((pl.col("ts") >= periodo[0]) & (pl.col("ts") <=  periodo[1]))
    return((df.group_by("master_metadata_album_artist_name")
        .agg([pl.col("s_played").sum()])
        .sort("s_played",descending=True)
        .select("*")
        .head(n)
))

def time_series(df):
        # Estrai anno e mese dalla colonna 'ts'
    df_new = df.with_columns(
        pl.col("ts").dt.year().alias("year"),
        pl.col("ts").dt.month().alias("month")
    )

    # Raggruppa per anno e mese e somma i secondi di ascolto
    grouped = df_new.group_by(["year", "month"]).agg(
        pl.col("s_played").sum().alias("total_seconds_played")
    )

    # Ordina i risultati per anno e mese
    grouped = grouped.sort(["year", "month"])
    grouped.write_csv("dati.time.series")
    
    return grouped
print("Serie temporale")
time_series(df)