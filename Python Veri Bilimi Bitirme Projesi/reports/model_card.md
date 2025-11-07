Boyut (satır, sütun): (7043, 21)

İlk 5 satır:
    customerID  gender  SeniorCitizen Partner Dependents  tenure PhoneService     MultipleLines  ... StreamingTV StreamingMovies        Contract PaperlessBilling              PaymentMethod MonthlyCharges TotalCharges Churn     
0  7590-VHVEG  Female              0     Yes         No       1           No  No phone service  ...          No              No  Month-to-month              Yes           Electronic check          29.85        29.85    No      
1  5575-GNVDE    Male              0      No         No      34          Yes                No  ...          No              No        One year               No               Mailed check          56.95       1889.5    No      
2  3668-QPYBK    Male              0      No         No       2          Yes                No  ...          No              No  Month-to-month              Yes               Mailed check          53.85       108.15   Yes      
3  7795-CFOCW    Male              0      No         No      45           No  No phone service  ...          No              No        One year               No  Bank transfer (automatic)          42.30      1840.75    No      
4  9237-HQITU  Female              0      No         No       2          Yes                No  ...          No              No  Month-to-month              Yes           Electronic check          70.70       151.65   Yes      

[5 rows x 21 columns]

Veri tipleri:
 customerID           object
gender               object
SeniorCitizen         int64
Partner              object
Dependents           object
tenure                int64
PhoneService         object
MultipleLines        object
InternetService      object
OnlineSecurity       object
OnlineBackup         object
DeviceProtection     object
TechSupport          object
StreamingTV          object
StreamingMovies      object
Contract             object
PaperlessBilling     object
PaymentMethod        object
MonthlyCharges      float64
TotalCharges         object
Churn                object
dtype: object

Eksik değer sayısı (ilk 10):
 customerID         0
gender             0
SeniorCitizen      0
Partner            0
Dependents         0
tenure             0
PhoneService       0
MultipleLines      0
InternetService    0
OnlineSecurity     0
dtype: int64

Hedef (Churn) dağılımı:
        count  ratio%
Churn
No      5174   73.46
Yes     1869   26.54

Kategorik sütunlar: ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'TotalCharges', 'Churn']
Sayısal sütunlar: ['SeniorCitizen', 'tenure', 'MonthlyCharges']

 Contract ile Churn İlişkisi
         Contract Churn  count  ratio%
0  Month-to-month    No   2220   57.29
1  Month-to-month   Yes   1655   42.71
2        One year    No   1307   88.73
3        One year   Yes    166   11.27
4        Two year    No   1647   97.17
5        Two year   Yes     48    2.83

 InternetService ile Churn İlişkisi
  InternetService Churn  count  ratio%
0             DSL    No   1962   81.04
1             DSL   Yes    459   18.96
2     Fiber optic    No   1799   58.11
3     Fiber optic   Yes   1297   41.89
4              No    No   1413   92.60
5              No   Yes    113    7.40

Korelasyon Matrisi (Churn_numeric ile en ilişkili):
Churn_numeric     1.000000
MonthlyCharges    0.193356
SeniorCitizen     0.150889
tenure           -0.352229
Name: Churn_numeric, dtype: float64

Sayısal sütunlar: ['SeniorCitizen', 'tenure', 'MonthlyCharges']
Kategorik sütunlar: ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'TotalCharges']

--- Model Sonuçları (Varsayılan Eşik = 0.5) ---
Accuracy: 0.7942
ROC-AUC: 0.8403

Classification Report:
               precision    recall  f1-score   support

          No       0.84      0.89      0.86      1035
         Yes       0.63      0.54      0.58       374

    accuracy                           0.79      1409
   macro avg       0.74      0.71      0.72      1409
weighted avg       0.79      0.79      0.79      1409


Confusion Matrix:
Confusion Matrix:
 [[917 118]
 [172 202]]

 [172 202]]


--- Yeni Eşik (0.35) Sonuçları ---
Accuracy: 0.7679
ROC-AUC: 0.8403

ROC-AUC: 0.8403


Classification Report:
               precision    recall  f1-score   support

          No       0.88      0.79      0.83      1035
         Yes       0.55      0.70      0.61       374

    accuracy                           0.77      1409
   macro avg       0.71      0.74      0.72      1409
weighted avg       0.79      0.77      0.78      1409


Confusion Matrix (Yeni Eşik):
 [[822 213]
 [114 260]]