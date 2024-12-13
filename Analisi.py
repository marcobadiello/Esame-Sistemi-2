from Estrattore import df
import polars as pl
from datetime import datetime

'''
In questo file vengono definite tutte le funzioni che hanno come
scopo un analisi dei dati pecifica e restituiscono i dati richiesti
'''

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
    
    # creo i dataframe della time series e dei peridoo di ascolo
    p = dataframe_periodi(df)
    d = time_series_scorretto(df)

    # creo le liste dei periodi
    lista_p = [f"{p["anno"][i]}-{p["mese"][i]}" for i in range(len(p))]
    lista_d = [f"{d["year"][i]}-{d["month"][i]}" for i in range(len(d))]

    # creo la lissta delle ore riprodotte
    vere_ore = []
    # converto la colonna in una liste perchè il progetto è mio e mi trovo meglio
    thp = d["total_hours_played"].to_list() 

    for periodo in lista_p:
        if periodo in lista_d:
            # mi asicuro che il valore sia floating point
            vere_ore.append(float(thp[lista_d.index(periodo)]))  
            # se l'artista non è peresente in quel mese assegno il valore 0.0 (float)
            vere_ore.append(0.0) 

    # aggiungi la colonna 'ore_riprodotte' con i valori corrispondenti a ogni riga
    df_finale = p.with_columns(
        pl.Series(name="ore_riprodotte", values=vere_ore)
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
    return (
        df.group_by(["year", "month"])  # Raggruppa per anno e mese
          .agg((pl.col("s_played").sum() / 3600).alias("total_hours_played"))  # Converti i secondi in ore
          .sort(["year", "month"])  # Ordina per anno e mese
    )
    
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
    
    # mi prendoo la time series classica
    data = time_series(df)
    
    # aggiungo la colonna con le ore cumulate
    data_cum = data.with_columns(
    (pl.col("ore_riprodotte").cum_sum()).alias("ore_riprodotte_cumulate")
    )
    
    # cancello tutte le colonne che non mi servono in modo che mi resti solamente la
    # colonna "peridoo" e "ore_riprodotte_cumulate"
    data_cum = data_cum.drop("anno")
    data_cum = data_cum.drop("mese")
    data_cum = data_cum.drop("ore_riprodotte")
    
    return data_cum





'''
COSE IMPORTANTI DA SAPERE
- Ogni periodo corrisponde ad un mese quindi ogni 12 periodi corrisponde un anno
'''