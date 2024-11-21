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
periodo = (datetime(2020, 1, 1),datetime(2020, 1, 31))
print(top_n_canzoni(df,15,periodo))