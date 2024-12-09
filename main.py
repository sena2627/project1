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
        return None

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
        except (json.JSONDecodeError, FileNotFoundError):
            print("Hatalı veya eksik JSON dosyası. Dosya sıfırlanıyor...")
            all_songs = []

    # Şarkının zaten kaydedilmiş olup olmadığını kontrol et
    for song in all_songs:
        if song["title"].lower() == song_details["title"].lower() and song["artist"].lower() == song_details["artist"].lower():
            print(f"{song_details['title']} zaten kaydedilmiş.")
            return song_details  # Zaten kayıtlıysa mevcut bilgileri döndür

    # Yeni şarkıyı listeye ekle
    all_songs.append(song_details)

    # Listeyi JSON formatında kaydet
    with open(all_songs_file, "w", encoding="utf-8") as file:
        json.dump(all_songs, file, ensure_ascii=False, indent=4)

    print(f"{song_name} başarıyla kaydedildi.")
    return song_details


# Şarkı Arama ve Analiz Fonksiyonu
def search_and_analyze(query):
    data_folder = "data"
    all_songs_file = os.path.join(data_folder, "all_songs.json")

    # Veri dosyasını kontrol et
    if not os.path.exists(all_songs_file):
        print("Veri dosyası bulunamadı. Yeni bir dosya oluşturuluyor.")
        with open(all_songs_file, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    # Şarkıları yükle
    try:
        with open(all_songs_file, "r", encoding="utf-8") as file:
            all_songs = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Hatalı veya boş JSON dosyası. Dosya sıfırlanıyor...")
        all_songs = []
        with open(all_songs_file, "w", encoding="utf-8") as file:
            json.dump(all_songs, file, ensure_ascii=False, indent=4)

    # Sorguya uygun şarkıları bul
    query_normalized = query.lower()
    matching_songs = []
    for song in all_songs:
        lyrics = song.get("lyrics", "").lower()
        if query_normalized in lyrics:
            count = lyrics.count(query_normalized)
            matching_songs.append({**song, "query_count": count})

    # Eğer şarkılar arasında kelime bulunuyorsa
    if matching_songs:
        # En çok geçen şarkıdan en aza sıralama
        matching_songs = sorted(matching_songs, key=lambda x: x["query_count"], reverse=True)
        print(f"\n'{query}' kelimesi geçen şarkılar (En çoktan en aza sıralı):")
        for song in matching_songs:
            print(f"Şarkı: {song['title']} - Sanatçı: {song['artist']}")
            print(f"Sözler:\n{song['lyrics']}\n")
            print(f"'{query}' kelimesi {song['query_count']} kez geçiyor.")
            print(f"Spotify URL: {song.get('spotify_url', 'Bulunamadı')}\n")
        return

    # Eğer kelime şarkılarda yoksa yeni şarkı ekle
    print(f"'{query}' kelimesi şarkılarda bulunamadı.")
    song_name = input("Eklenecek şarkının adını girin: ")
    artist_name = input("Eklenecek şarkının sanatçısını girin (opsiyonel): ")

    new_song = save_song_data(song_name, artist_name)

    if new_song:
        # Yeni şarkı eklenince kelimeyi tekrar kontrol et
        print(f"\n'{query}' kelimesi yeni şarkı eklendikten sonra tekrar analiz ediliyor...\n")
        search_and_analyze(query)
    else:
        print("Şarkı eklenirken hata oluştu.")


# Kullanıcıdan sorgu alıp şarkı bilgilerini kaydet veya arama yap
if __name__ == "__main__":
    query = input("Aramak istediğiniz kelimeyi girin: ")
    search_and_analyze(query)
