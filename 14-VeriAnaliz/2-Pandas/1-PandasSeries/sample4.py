import numpy as np
import pandas as pd

ser2017 = pd.Series([500,600,1400,2000,3000],["Pantolon","Ceket","Şort","Atlet" ,"Çorap"])
ser2018 = pd.Series([200,180,1200,700,2500],["Pantolon","Ceket","Şort","Atlet" ,"Pijama"])
print(ser2017)
print(ser2018)

print(ser2017["Ceket"])
print(ser2018["Atlet"])
print(ser2017+ser2018)
toplam = ser2017+ser2018
print(toplam)
print(toplam["Ceket"])
print(toplam["Çorap"])