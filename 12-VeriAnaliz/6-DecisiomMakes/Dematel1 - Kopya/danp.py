import numpy as np

T = np.array([
    [0.29, 1.04, 0.81],
    [0.39, 0.45, 0.72],
    [0.16, 0.62, 0.29]
])
# Sütun bazlı normalizasyon (ANP süpermatrisi)
column_sums = T.sum(axis=0)
W = T / column_sums

print("Ağırlıklı Süpermatris (W):\n", np.round(W, 4))
def limit_supermatrix(W, max_iter=200):
    W_lim = W.copy()
    for _ in range(max_iter):
        W_lim = W_lim @ W
        print(W_lim)
    return W_lim

W_limit = limit_supermatrix(W)

print("Limit Süpermatris:\n", np.round(W_limit, 4))
weights = W_limit[:, 0]
weights = weights / weights.sum()  # garanti normalizasyon

criteria = ["Fiyat", "Kalite", "Teslimat"]

print("\nNihai Kriter Ağırlıkları (DANP):")
for c, w in zip(criteria, weights):
    print(f"{c}: {w:.4f}")
