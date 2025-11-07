import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)

plt.rcParams["figure.figsize"] = (6, 4)
plt.style.use("default")


## VERİYİ OKUMA VE İLK İNCELEME

path = "Customer-Churn.csv"
df = pd.read_csv(path)

print("Boyut (satır, sütun):", df.shape)
print("\nİlk 5 satır:\n", df.head())
print("\nVeri tipleri:\n", df.dtypes)

# Eksik değer kontrolü
na_counts = df.isna().sum().sort_values(ascending=False)
print("\nEksik değer sayısı (ilk 10):\n", na_counts.head(10))

# Hedef değişken dağılımı
target_counts = df["Churn"].value_counts()
target_ratio = (target_counts / len(df) * 100).round(2)
print("\nHedef (Churn) dağılımı:\n", pd.DataFrame({"count": target_counts, "ratio%": target_ratio}))

# Hedef dağılımını çubuk grafikle gösterelim
plt.bar(target_counts.index, target_counts.values, color=["skyblue", "salmon"])
plt.title("Churn Dağılımı")
plt.xlabel("Churn (Yes / No)")
plt.ylabel("Adet")
plt.tight_layout()
plt.show()


## KATEGORİK VE SAYISAL SÜTUNLARIN İLİŞKİLERİ


# Hedefi 0/1 e dönüştürme
df["Churn_numeric"] = df["Churn"].map({"Yes": 1, "No": 0})

# Kategorik sütunları seç
cat_cols = [c for c in df.columns if df[c].dtype == "object" and c != "customerID"]
print("\nKategorik sütunlar:", cat_cols)

# Sayısal sütunları seç
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols = [c for c in num_cols if c != "Churn_numeric"]
print("Sayısal sütunlar:", num_cols)

# Kategorik değişkenler ile Churn ilişkisi
def show_churn_by_category(column_name):
    tablo = df.groupby([column_name, "Churn"]).size().reset_index(name="count")
    tablo["ratio%"] = (
        tablo.groupby(column_name)["count"]
        .apply(lambda x: (x / x.sum() * 100).round(2))
        .reset_index(drop=True)
    )
    print(f"\n {column_name} ile Churn İlişkisi")
    print(tablo)

    # Basit çubuk grafiği
    churn_yes = tablo[tablo["Churn"] == "Yes"]
    churn_no = tablo[tablo["Churn"] == "No"]

    x = np.arange(len(churn_yes[column_name]))
    width = 0.35

    plt.bar(x - width/2, churn_no["ratio%"], width, label="No", color="lightblue")
    plt.bar(x + width/2, churn_yes["ratio%"], width, label="Yes", color="salmon")
    plt.xticks(x, churn_yes[column_name], rotation=45, ha="right")
    plt.title(f"{column_name} - Churn Oranı (%)")
    plt.xlabel(column_name)
    plt.ylabel("Oran (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Örnek kategorik değişken analizleri
show_churn_by_category("Contract")
show_churn_by_category("InternetService")

# Sayısal değişkenler için boxplot grafikleri
for col in num_cols:
    churn_no = df[df["Churn"] == "No"][col]
    churn_yes = df[df["Churn"] == "Yes"][col]
    plt.boxplot([churn_no, churn_yes], labels=["No", "Yes"])
    plt.title(f"{col} değişkenine göre Churn dağılımı")
    plt.ylabel(col)
    plt.show()


## KORELASYON ANALİZİ

corr = df[num_cols + ["Churn_numeric"]].corr()
print("\nKorelasyon Matrisi (Churn_numeric ile en ilişkili):")
print(corr["Churn_numeric"].sort_values(ascending=False))

plt.imshow(corr, cmap="coolwarm", interpolation="none")
plt.colorbar(label="Korelasyon")
plt.title("Korelasyon Isı Haritası")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
plt.yticks(range(len(corr.columns)), corr.columns)
plt.tight_layout()
plt.show()


## LOGISTIC REGRESSION


# Girdi / hedef ayrımı
X = df.drop(columns=["Churn", "Churn_numeric", "customerID"])
y = df["Churn"].map({"Yes": 1, "No": 0})

# Sayısal ve kategorik sütunlar
numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

print("\nSayısal sütunlar:", numeric_features)
print("Kategorik sütunlar:", categorical_features)

# Ön işleme (Scaler + OneHotEncoder)
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# Model nesnesi
lojistik_model = LogisticRegression(max_iter=1000, solver="lbfgs")

# Pipeline (ön işleme + model)
is_akisi = Pipeline(steps=[("onisleme", preprocessor), ("model", lojistik_model)])

# Eğitim / test bölünmesi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Modeli eğit
is_akisi.fit(X_train, y_train)

# Tahmin ve olasılıklar
y_pred = is_akisi.predict(X_test)
y_prob = is_akisi.predict_proba(X_test)[:, 1]

# Performans metrikleri
print("\n--- Model Sonuçları (Varsayılan Eşik = 0.5) ---")
print("Accuracy:", (y_pred == y_test).mean().round(4))
print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 4))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=["No", "Yes"]))

# Karışıklık matrisi
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)

# ROC eğrisi çizimi
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.plot(fpr, tpr, label="ROC Curve", color="darkorange")
plt.plot([0, 1], [0, 1], "--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Eğrisi")
plt.legend()
plt.show()


## EŞİK ANALİZİ 

threshold = 0.35
y_pred_thresh = (y_prob >= threshold).astype(int)

print(f"\n--- Yeni Eşik ({threshold}) Sonuçları ---")
print("Accuracy:", (y_pred_thresh == y_test).mean().round(4))
print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 4))
print("\nClassification Report:\n", classification_report(y_test, y_pred_thresh, target_names=["No", "Yes"]))

cm_thresh = confusion_matrix(y_test, y_pred_thresh)
print("\nConfusion Matrix (Yeni Eşik):\n", cm_thresh)

"""
# SONUÇ ve DEĞERLENDİRME

- Veri setinde toplam 7043 müşteri bulunuyor, bunların %26.5’i (1869 kişi) hizmetten ayrılmış (Churn = Yes).
- Korelasyon sonuçlarına göre:
  - tenure (müşterinin şirkette kalma süresi) churn ile negatif ilişkili (-0.35). Yani şirkette daha uzun kalan müşteriler daha az ayrılıyor.
  - MonthlyCharges (aylık ücret) churn ile pozitif ilişkili (0.19). Aylık ödemesi yüksek olan müşteriler daha fazla ayrılıyor.
  - SeniorCitizen değişkeni de churn ile zayıf pozitif ilişki gösteriyor (yaşlı müşteriler biraz daha fazla ayrılıyor olabilir).

- Logistic Regression modeli genel olarak %79 doğruluk ve %0.84 ROC-AUC skoruna ulaştı.

- Varsayılan eşik (0.5) altında model “No” sınıfını (churn etmeyenleri) daha iyi tahmin etti.
  Ancak eşik 0.35’e indirildiğinde Recall (Yes sınıfı için) %54’ten %70’e yükseldi.
  Bu da churn eden müşterileri yakalamada daha iyi bir sonuç verdi.

- İş açısından bakıldığında, yüksek aylık ücret ödeyen ve kısa süreli müşteriler churn açısından riskli gruptur.
"""
