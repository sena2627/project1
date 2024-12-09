import os
import json
from utils import get_song_lyrics, get_spotify_url

# JSON Verilerini Kaydetme
def save_song_data(song_name, artist_name=None):
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

    # Şarkı bilgilerini çek
    song_details = get_song_lyrics(song_name, artist_name)
    if not song_details:
        print("Şarkı bilgileri bulunamadı.")
        return
    
    # Spotify bağlantısını ekle
    spotify_url = get_spotify_url(song_name, artist_name)
    if spotify_url:
        song_details["spotify_url"] = spotify_url
    else:
        print("Spotify bağlantısı alınamadı.")
        return

    # Tüm şarkı verilerini bir listeye ekle
    all_songs_file = os.path.join(data_folder, "all_songs.json")
    if os.path.exists(all_songs_file):
        with open(all_songs_file, "r", encoding="utf-8") as file:
            all_songs = json.load(file)
    else:
        all_songs = []

    # Yeni şarkıyı listeye ekle
    all_songs.append(song_details)

    # Listeyi JSON formatında kaydet
    with open(all_songs_file, "w", encoding="utf-8") as file:
        json.dump(all_songs, file, ensure_ascii=False, indent=4)

    print(f"{song_name} başarıyla kaydedildi.")

# Kullanıcıdan sorgu alıp şarkı bilgilerini kaydet
if __name__ == "__main__":
    song_name = input("Şarkı Adı Girin: ")
    artist_name = input("Sanatçı Adı (opsiyonel): ")
    save_song_data(song_name, artist_name)
