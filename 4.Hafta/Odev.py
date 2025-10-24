import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("train.csv")

# veri setleri hakkında bilig aldık 
result=df.head(40)
#result=df.info()
result=df.describe()

# inceleyeceğimiz sütunlarda boş veri var mı kontrol ettik
print("GrLivArea boş:", df["GrLivArea"].isnull().sum())     # 0
print("OverallQual boş:", df["OverallQual"].isnull().sum()) # 0
print("SalePrice boş:", df["SalePrice"].isnull().sum())     # 0

# Sadece model için gerekli 3 sütunu filtreledik
df=df[['GrLivArea', 'OverallQual', 'SalePrice']]

# Eksik satırları sildik 
df=df.dropna()

# İsteğe bağlı hız için yorum satırı kaldırılabilir
#df=df.head() 

# Bağımsız (X) ve bağımlı (Y) değişkenleri belirledik
X=df[["GrLivArea", "OverallQual"]]
Y=df["SalePrice"]

# Model nesnesi oluşturuldu
model=LinearRegression()

# Model eğitildi
model.fit(X,Y)

# Modelin katsayıları ve sabit terimi yazdırıldı
print("Katsayılar (coefficients):", model.coef_)
print("Sabit terim (intercept):", model.intercept_)

# Tahminler alındı
y_pred=model.predict(X)

# R^2 skoru hesaplandı
r2=r2_score(Y, y_pred)
print("R-kare: ", r2)

# Ortalama Mutlak Hata hesaplandı
mae=mean_absolute_error(Y, y_pred)
print("Ortalama mutlak hata: ", mae)

rmse=np.sqrt(mean_squared_error(Y, y_pred))
print("Kök ortalama kare hatası: ", rmse)


# Yaşanabilir Alan - Satış Fiyatı ilişkisi 
plt.figure(figsize=(8, 6))
sns.regplot(x="GrLivArea", y="SalePrice", data=df, line_kws={"color":"red"})
plt.title("GrLivArea vs SalePrice")
plt.xlabel("Yaşanabilir Alan (GrLivArea)")
plt.ylabel("Satış Fiyatı (SalePrice)")
plt.grid(True)
plt.show()

# Genel Kalite Puanı - Satış Fiyatı ilişkisi
plt.figure(figsize=(8, 6))
sns.boxplot(x="OverallQual", y="SalePrice", data=df)
plt.title("OverallQual vs SalePrice")
plt.xlabel("Genel Kalite Puanı (OverallQual)")
plt.ylabel("Satış Fiyatı (SalePrice)")
plt.grid(True)
plt.show()
