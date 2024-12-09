import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Kimlik Bilgileri
SPOTIFY_CLIENT_ID = "6ca7fbbd2e80456fa8e46225699bbbdc"  # Spotify Client ID'nizi buraya yazın
SPOTIFY_CLIENT_SECRET = "22e45d9962894bde9d1807de5fd3a9d2"  # Spotify Client Secret'ınızı buraya yazın

# Genius API Anahtarı
GENIUS_API_KEY = "4KBzJjaPY1SStmY5jDlGLLpbOfVZlnnn_1K_dat_m4AdlCPU0gH1qCA4PPV05SEbs0J37ySa6-N7h0LifehShg"

# Şarkı Sözlerini Genius API'den Çekme
def get_song_lyrics(song_name, artist_name=None):
    genius = lyricsgenius.Genius(GENIUS_API_KEY)
    
    try:
        if artist_name:
            song = genius.search_song(song_name, artist_name)
        else:
            song = genius.search_song(song_name)
        
        if song:
            return {"title": song.title, "artist": song.artist, "lyrics": song.lyrics}
        else:
            return None
    except Exception as e:
        print(f"Hata (Genius API): {e}")
        return None

# Spotify URL'sini Spotipy ile Çekme
def get_spotify_url(song_name, artist_name=None):
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
    
    try:
        query = f"{song_name} {artist_name}" if artist_name else song_name
        results = spotify.search(q=query, type="track", limit=1)
        
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["external_urls"]["spotify"]
        else:
            return None
    except Exception as e:
        print(f"Hata (Spotify API): {e}")
        return None
