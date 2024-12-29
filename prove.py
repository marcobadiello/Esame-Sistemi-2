
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Le tue credenziali Spotify
client_id = 'fca40934bfc94188b06e4d95d42d0dcb'
client_secret = '45acdbe55d954d20a55e2c8db28b7035'

# Autenticazione
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Nome dell'artista
artist_name = 'Adele'

# Cerca l'artista
result = sp.search(q=artist_name, type='artist', limit=1)

# Estrai e stampa l'URL della foto profilo
artist = result['artists']['items'][0]
profile_image_url = artist['images'][0]['url']
print(f"URL della foto profilo: {profile_image_url}")
