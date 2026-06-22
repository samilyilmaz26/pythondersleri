import numpy as np

# 1. Doğrudan ilişki matrisi (A)
A = np.array([
    [0, 3, 2],
    [1, 0, 2],
    [0, 2, 0]
], dtype=float)

# 2. Normalizasyon
row_sums = A.sum(axis=1)
col_sums = A.sum(axis=0)
s = 1 / max(row_sums.max(), col_sums.max())

# // Normalizasyon işlemi
X = s * A 
print(X)

# 3. Toplam ilişki matrisi
# I I ıdentity matrix, T = X(I - X)^(-1) formülü ile hesaplanır
# T Toplam ilişki matrisi, doğrudan ve dolaylı etkileri içerir. (I - X)^{-1} ifadesi, X'in etkilerini hesaba katarak toplam etkileri hesaplar.
I = np.eye(A.shape[0])
T = X @ np.linalg.inv(I - X)

# 4. D ve R değerleri
D = T.sum(axis=1)  # satır toplamları
R = T.sum(axis=0)  # sütun toplamları

# 5. Sonuçları yazdır
criteria = ["Fiyat", "Kalite", "Teslimat"]

print("Normalize Edilmiş Matris (X):\n", np.round(X, 3), "\n")
print("Toplam İlişki Matrisi (T):\n", np.round(T, 3), "\n")

print(D)

print("Kriter Bazlı Sonuçlar:")
for i in range(len(criteria)):
    print(f"{criteria[i]} -> D: {D[i]:.3f}, R: {R[i]:.3f}, D-R: {D[i]-R[i]:.3f}")

