import lyricsgenius

# Genius API Token'ınızı buraya yapıştırın
genius = lyricsgenius.Genius("4KBzJjaPY1SStmY5jDlGLLpbOfVZlnnn_1K_dat_m4AdlCPU0gH1qCA4PPV05SEbs0J37ySa6-N7h0LifehShg")

# Şarkı arama işlemi
song = genius.search_song("Bohemian Rhapsody", "Queen")

if song:
    print(f"Şarkı Adı: {song.title}")
    print(f"Sanatçı: {song.artist}")
    print("\nŞarkı Sözleri:\n")
    print(song.lyrics)
else:
    print("Şarkı bulunamadı!")

