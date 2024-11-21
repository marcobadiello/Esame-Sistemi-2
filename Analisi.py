from Estrattore import df
import polars as pl

# def top(n=10,chiave="song",periodo=""):
    
def top_n_canzoni(n):
    return((df.group_by("master_metadata_track_name")
        .agg([pl.col("s_played").sum(),
             pl.col("spotify_track_uri").first()])
        .sort("s_played",descending=True)
        .select("*")
        .head(n)
))
    
