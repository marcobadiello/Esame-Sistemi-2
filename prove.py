import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Sostituisci questi valori con le tue credenziali dell'applicazione Spotify
client_id = 'xxx'
client_secret = 'xxx'

# Autenticazione con Spotify usando il Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
