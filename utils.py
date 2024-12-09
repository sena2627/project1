import os
import json
import lyricsgenius

def get_song_lyrics(title, artist):
    """Genius API'den şarkı sözlerini alır."""
    genius_api_key = os.getenv("GENIUS_API_KEY")
    genius = lyricsgenius.Genius(genius_api_key)
    
    try:
        song = genius.search_song(title, artist)
        if song:
            return {
                "title": song.title,
                "artist": song.artist,
                "lyrics": song.lyrics,
                "spotify_url": song.url
            }
        else:
            return None
    except Exception as e:
        print(f"Şarkı sözlerini alırken hata oluştu: {e}")
        return None

def save_song_to_json(song_data):
    """Şarkıyı JSON dosyasına kaydeder."""
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)
    all_songs_file = os.path.join(data_folder, "all_songs.json")
    
    # JSON dosyasını yükle veya yeni bir liste oluştur
    if os.path.exists(all_songs_file):
        with open(all_songs_file, "r", encoding="utf-8") as file:
            all_songs = json.load(file)
    else:
        all_songs = []
    
    # Şarkının zaten kaydedilmiş olup olmadığını kontrol et
    for existing_song in all_songs:
        if existing_song["title"] == song_data["title"] and existing_song["artist"] == song_data["artist"]:
            print("Bu şarkı zaten kayıtlı.")
            return
    
    # Yeni şarkıyı ekle
    all_songs.append(song_data)
    with open(all_songs_file, "w", encoding="utf-8") as file:
        json.dump(all_songs, file, ensure_ascii=False, indent=4)
    print(f"'{song_data['title']}' şarkısı kaydedildi.")

def search_and_analyze(query):
    """Şarkı sözlerinde verilen sorguyu arar."""
    data_folder = "data"
    all_songs_file = os.path.join(data_folder, "all_songs.json")
    
    if not os.path.exists(all_songs_file):
        print("Veri dosyası bulunamadı. Yeni dosya oluşturulacak.")
        with open(all_songs_file, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
    
    with open(all_songs_file, "r", encoding="utf-8") as file:
        all_songs = json.load(file)
    
    matching_songs = []
    query_normalized = query.lower().replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")
    
    for song in all_songs:
        lyrics = song.get("lyrics", "").lower()
        lyrics_normalized = lyrics.replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")
        if query_normalized in lyrics_normalized:
            count = lyrics_normalized.count(query_normalized)
            matching_songs.append({**song, "query_count": count})
    
    if not matching_songs:
        print(f"'{query}' kelimesi şarkılarda bulunamadı. Yeni şarkı eklenebilir.")
        title = input("Şarkının adını girin: ")
        artist = input("Sanatçının adını girin: ")
        
        # Şarkıyı Genius API'den al ve JSON dosyasına ekle
        song_data = get_song_lyrics(title, artist)
        if song_data:
            save_song_to_json(song_data)
            print(f"'{query}' kelimesini içeren şarkı araması için tekrar deneyin.")
        else:
            print("Şarkı bulunamadı veya eklenemedi.")
        return
    
    # En çok geçen kelimeyi bul
    top_song = max(matching_songs, key=lambda x: x["query_count"])
    
    # Sonuçları yazdır
    print(f"En çok '{query}' kelimesi geçen şarkı:")
    print(f"- Şarkı: {top_song['title']} by {top_song['artist']}")
    print(f"- Geçiş Sayısı: {top_song['query_count']}")
    print(f"- Spotify URL: {top_song.get('spotify_url', 'Bulunamadı')}\n")
    
    print("Diğer şarkılar:")
    for song in matching_songs:
        print(f"- {song['title']} by {song['artist']} (Geçiş Sayısı: {song['query_count']})")
