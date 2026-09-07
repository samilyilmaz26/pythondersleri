import matplotlib.pyplot as plt
import numpy as np

criteria = ["Fiyat", "Kalite", "Teslimat"]

# Daha önce hesaplanan D ve R
D = np.array([2.14, 1.56, 1.07])
R = np.array([0.84, 2.11, 1.82])

D_minus_R = D - R
D_plus_R = D + R

plt.figure(figsize=(8,6))
plt.axvline(0, linestyle='--')
plt.axhline(np.mean(D_plus_R), linestyle='--')

plt.scatter(D_minus_R, D_plus_R)

for i, txt in enumerate(criteria):
    plt.text(D_minus_R[i] + 0.02, D_plus_R[i] + 0.02, txt)

plt.xlabel("D − R (Sebep / Sonuç)")
plt.ylabel("D + R (Toplam Önem)")
plt.title("DEMATEL Sebep–Sonuç Diyagramı")

plt.grid(True)
plt.show()
