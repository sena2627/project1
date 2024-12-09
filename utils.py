import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Genius API Ayarları
genius = lyricsgenius.Genius("4KBzJjaPY1SStmY5jDlGLLpbOfVZlnnn_1K_dat_m4AdlCPU0gH1qCA4PPV05SEbs0J37ySa6-N7h0LifehShg")  # Buraya kendi Genius API anahtarınızı yapıştırın

# Spotify API Ayarları
client_id = "6ca7fbbd2e80456fa8e46225699bbbdc"  # Spotify client ID'nizi buraya yapıştırın
client_secret = "22e45d9962894bde9d1807de5fd3a9d2"  # Spotify secret key'inizi buraya yapıştırın
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Genius API ile Şarkı Sözlerini Çekme
def get_song_lyrics(song_name, artist_name=None):
    song = genius.search_song(song_name, artist_name)
    if song:
        return {"title": song.title, "artist": song.artist, "lyrics": song.lyrics}
    return None

# Spotify API ile Şarkı URL'sini Çekme
def get_spotify_url(song_name, artist_name=None):
    query = f"{song_name} {artist_name}" if artist_name else song_name
    results = sp.search(q=query, type="track", limit=1)
    if results.get("tracks") and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track.get("external_urls", {}).get("spotify", None)
    return None

# Şarkı Arama Fonksiyonu
def search_songs(query):
    data_folder = "data"
    results = []

    if not os.path.exists(data_folder):
        print("Veri klasörü bulunamadı.")
        return

    for filename in os.listdir(data_folder):
        if filename.endswith(".json") and filename != "all_songs.json":
            file_path = os.path.join(data_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                song_data = json.load(file)
                if "lyrics" in song_data and query.lower() in song_data["lyrics"].lower():
                    results.append(song_data)

    if results:
        print("Arama Sonuçları:")
        for song in results:
            print(f"- {song['title']} by {song['artist']}")
            print(f"Spotify URL: {song.get('spotify_url', 'Bulunamadı')}\n")
    else:
        print("Şarkı bulunamadı.")
