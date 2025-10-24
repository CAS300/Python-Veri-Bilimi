import pandas as pd

# Verileri oku (ilk birkaç satır alınarak test için kısıtlama yapıldı)
df_basics = pd.read_csv("title.basics.tsv.gz", sep="\t", compression="gzip", na_values="\\N", dtype="str", nrows=400000)
df_ratings = pd.read_csv("title.ratings.tsv.gz", sep="\t", compression="gzip", na_values="\\N", dtype="str", nrows=400)

# Sayısal dönüşümler
df_basics["runtimeMinutes"] = pd.to_numeric(df_basics["runtimeMinutes"], errors="coerce")
df_basics["startYear"] = pd.to_numeric(df_basics["startYear"], errors="coerce")
df_basics["endYear"] = pd.to_numeric(df_basics["endYear"], errors="coerce")
df_ratings["averageRating"] = pd.to_numeric(df_ratings["averageRating"], errors="coerce").astype("float64")
df_ratings["numVotes"] = pd.to_numeric(df_ratings["numVotes"], errors="coerce").astype("int64")

# Sadece filmleri seç
sadece_title = df_basics[df_basics['titleType'] == "movie"]

# 2000–2024 arası yılları filtrele
startYear_2000_2024 = df_basics[(df_basics["startYear"] >= 2000) & (df_basics["startYear"] <= 2024)]

# Aykırı süreleri NaN yap (negatif, 0 veya >300 dakika)
df_basics.loc[(df_basics["runtimeMinutes"] <= 0) | (df_basics["runtimeMinutes"] > 300), "runtimeMinutes"] = pd.NA

# İki veri setini tconst üzerinden inner join ile birleştir
df_merged = pd.merge(df_basics, df_ratings, on="tconst", how="inner")

# genres sütununu virgülle ayır ve satırlara böl (explode)
df_merged['genres'] = df_merged['genres'].str.split(',')
df_exploded = df_merged.explode('genres')

# Tür bazlı istatistikler
genre_group = df_exploded.groupby('genres')
avg_rating = genre_group['averageRating'].mean()          # Ortalama puan
median_runtime = genre_group['runtimeMinutes'].median()   # Medyan süre
count_movies = genre_group.size()                         # Toplam film sayısı

# En çok oylanan ilk 3 film (global olarak)
top3_votes = df_merged.head(3)[['primaryTitle', 'startYear', 'averageRating', 'numVotes']]

# Özet tablo
summary_df = pd.DataFrame({
    'Ortalama puan': avg_rating,
    'Medyan süre': median_runtime,
    'Toplam film': count_movies
})

# 5000+ oy alan filmlerle çalış
df_filtered = df_merged[df_merged['numVotes'] >= 5000]

# En yüksek puanlı 20 film (puanına göre sıralanmış)
top20_rated = df_filtered.sort_values('averageRating', ascending=False).head(20)[['primaryTitle', 'startYear', 'averageRating', 'numVotes']]
