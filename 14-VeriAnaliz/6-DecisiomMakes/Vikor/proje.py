import numpy as np
import pandas as pd

# Karar matrisi
data = np.array([
    [250, 7, 5],
    [200, 8, 7],
    [300, 9, 6]
])

alternatives = ["A1", "A2", "A3"]
criteria = ["Fiyat", "Kalite", "Teslimat"]

# Kriter ağırlıkları
weights = np.array([0.4, 0.35, 0.25])

# Kriter türü (1 = fayda, -1 = maliyet)
criteria_type = np.array([-1, 1, 1])

# En iyi ve en kötü değerler
best = np.zeros(data.shape[1])
worst = np.zeros(data.shape[1])

for j in range(data.shape[1]):
    if criteria_type[j] == 1:
        best[j] = data[:, j].max()
        worst[j] = data[:, j].min()
    else:
        best[j] = data[:, j].min()
        worst[j] = data[:, j].max()

# S ve R hesaplama
S = []
R = []

for i in range(data.shape[0]):
    values = weights * (best - data[i]) / (best - worst)
    S.append(values.sum())
    R.append(values.max())

S = np.array(S)
R = np.array(R)

# Q hesaplama
v = 0.5
S_best, S_worst = S.min(), S.max()
R_best, R_worst = R.min(), R.max()

Q = v * (S - S_best) / (S_worst - S_best) + (1 - v) * (R - R_best) / (R_worst - R_best)

# Sonuç tablosu
result = pd.DataFrame({
    "Alternatif": alternatives,
    "S": S,
    "R": R,
    "Q": Q
})

print(result.sort_values("Q"))
