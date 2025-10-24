import numpy as np

np.random.seed(42)
tablo=np.random.randn(1000, 5)

min_value=tablo.max(axis=0)
max_value=tablo.min(axis=0)
norm=(tablo-min_value)/(max_value-min_value)

esik_deger=0.5
binary_data=(tablo>esik_deger).astype(int)

kategori_tablo = np.empty_like(tablo, dtype=object)  # Boş tablo hazırladım

kategori_tablo[tablo<=-1]="Düşük"
kategori_tablo[(tablo>-1)&(tablo<=1)] ="Orta"
kategori_tablo[tablo>1]="Yüksek"

print("Kategori Tablosu (İlk 5 Satır):\n", kategori_tablo[:5])

# Benzersiz kategoriler
kategoriler=np.unique(kategori_tablo)
print("\nBenzersiz Kategoriler:", kategoriler)

# Her kategoriye bir sayı
kategori_to_sayi = {k:i for i, k in enumerate(kategoriler)}
print("\nKategori -> Sayı eşleşmeleri:", kategori_to_sayi)

# Label encoded tablo 
label_encoded=np.vectorize(lambda x: kategori_to_sayi[x])(kategori_tablo)
print("\nLabel Encoded (İlk 5 Satır):\n", label_encoded[:5])

# One-hot encoding 
# (Kategoriler: 0 = Düşük, 1 = Orta, 2 = Yüksek)
one_hot=np.eye(len(kategoriler))[label_encoded]
print("\nOne-Hot Encoded (İlk 1 Satır):\n", one_hot[0])

mean_row=tablo.mean(axis=1, keepdims=True)  # Her satırın ortalaması
std_row=tablo.std(axis=1, keepdims=True)    # Her satırın std sapması

zscore_normalized=(tablo - mean_row) / std_row

print("Z-score Normalizasyonu (İlk 5 Satır):\n", zscore_normalized[:5])


#####
arr_arange=np.arange(10)         # 0'dan 9'a kadar tam sayılardan oluşan 1D dizi
arr_linspace=np.linspace(0, 1, 5) # 0 ile 1 arasında eşit aralıklı 5 sayıdan oluşan dizi
arr_zeros=np.zeros((3, 3))       # 3x3 boyutunda, tüm elemanları 0 olan matris
arr_ones=np.ones((2, 4))         # 2x4 boyutunda, tüm elemanları 1 olan matris
arr_eye=np.eye(5)                # 5x5 boyutunda, birim (köşegenleri 1, diğerleri 0) matrisi
#####

# Maske: tablo elemanları 0'dan büyük olanlar True, diğerleri False
maske=tablo>0

# Maske kullanarak sadece 0'dan büyük elemanları seçiyoruz
filtrelenmis=tablo[maske]

print("Filtrelenmiş elemanlar (ilk 10):", filtrelenmis[:10])


# Eksik değer simülasyonu
nan_sayisi = int(tablo.size * 0.01)  # %1 kadar NaN

# rastgele indisler
nan_indeksler = (np.random.randint(0, tablo.shape[0], nan_sayisi), np.random.randint(0, tablo.shape[1], nan_sayisi))

# NaN atama
tablo[nan_indeksler]=np.nan

print(f"NaN sayısı: {np.isnan(tablo).sum()}")  # Kaç NaN olduğunu kontrol et

# 2. Eksik değer doldurma (ortalama ile)
# Her sütunun ortalaması (NaN'ları göz ardı eder)
sutun_ortalari=np.nanmean(tablo, axis=0)

# NaN olan yerlerin indekslerini bulup ortalama ile doldurma
for i in range(tablo.shape[1]):
    nan_lar=np.isnan(tablo[:, i])
    tablo[nan_lar, i]=sutun_ortalari[i]
