import os
import json
from utils import get_song_lyrics, get_spotify_url, search_and_analyze

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
    
    # Tüm şarkı verilerini bir listeye ekle
    all_songs_file = os.path.join(data_folder, "all_songs.json")
    all_songs = []
    
    if os.path.exists(all_songs_file):
        try:
            with open(all_songs_file, "r", encoding="utf-8") as file:
                all_songs = json.load(file)
        except json.JSONDecodeError:
            print("Hatalı JSON formatı. Dosya sıfırlanacak.")

    # Yeni şarkıyı listeye ekle
    all_songs.append(song_details)

    # Listeyi JSON formatında kaydet
    with open(all_songs_file, "w", encoding="utf-8") as file:
        json.dump(all_songs, file, ensure_ascii=False, indent=4)

    print(f"{song_name} başarıyla kaydedildi.")

# Kullanıcıdan sorgu alıp şarkı bilgilerini kaydet veya arama yap
if __name__ == "__main__":
    mode = input("Mod Seçin: [1] Şarkı Ekle | [2] Şarkı Ara\nSeçiminiz: ")

    if mode == "1":
        song_name = input("Şarkı Adı Girin: ")
        artist_name = input("Sanatçı Adı (opsiyonel): ")
        save_song_data(song_name, artist_name)
    elif mode == "2":
        query = input("Aramak istediğiniz kelimeyi girin: ")
        search_and_analyze(query)
    else:
        print("Geçersiz seçim.")
