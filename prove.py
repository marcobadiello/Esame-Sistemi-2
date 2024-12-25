import spotipy
from spotipy.oauth2 import SpotifyOAuth
import Analisi as anal
from Estrattore import df


# Sostituisci con le tue credenziali
client_id = '0c495503d007492cb9ab221bc097e13c'
client_secret = 'd03ba7bbe9f749d0b47bea40a0f11882'
redirect_uri = 'http://localhost:8888/callback'

# Autenticazione con Spotify usando il OAuth Flow
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read"))

# Funzione per ottenere i generi dato un nome artista
def get_artist_genres(artist_name):
    # Cerca l'artista per nome
    search_result = sp.search(q=artist_name, type='artist', limit=1)

    if search_result['artists']['items']:
        # Ottieni le informazioni dell'artista
        artist_info = search_result['artists']['items'][0]
        genres = artist_info.get('genres', [])
        return genres if genres else "Nessun genere trovato"
    else:
        return "Artista non trovato"



data = anal.top_n_artisti(df,n=100)

info = {}
for row in data.iter_rows():
    artist_name = row[0]
    info[artist_name] = get_artist_genres(artist_name)
    print(artist_name,'---',info[artist_name])
print(info)