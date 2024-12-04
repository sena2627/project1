import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API kimlik bilgilerinizi buraya ekleyin
client_id = '6ca7fbbd2e80456fa8e46225699bbbdc'
client_secret = '22e45d9962894bde9d1807de5fd3a9d2'

# Spotify istemci kimlik doğrulama
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Şarkı arama
song_name = "Bohemian Rhapsody"
results = sp.search(q=song_name, type="track", limit=1)

if results["tracks"]["items"]:
    track = results["tracks"]["items"][0]
    print(f"Şarkı Adı: {track['name']}")
    print(f"Sanatçı: {track['artists'][0]['name']}")
    print(f"Albüm: {track['album']['name']}")
    print(f"Spotify Linki: {track['external_urls']['spotify']}")
else:
    print("Şarkı bulunamadı.")


