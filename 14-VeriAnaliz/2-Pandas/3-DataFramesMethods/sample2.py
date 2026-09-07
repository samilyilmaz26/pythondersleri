import numpy as np
import pandas as pd
from numpy.random import randn
 
df = pd.DataFrame(randn(3,3)*10,index = ["S1","S2","S3"],columns = ["Ocak","Şubat","Mart"])
print(df)
# Kolon Ekleme 
# 1. Yöntem

# df["Nisan "] = pd.Series(randn(3)*10,index = ["S1","S2","S3"]  )
# print(df)

# 2. Yöntem
# df["Nisan"] = randn(4)*100
# print(df)

# df["Nisan"] = ["100","200","500"]
# print(df)

# print(df.set_index("Mart"))
# print(df)

df.set_index("Mart", inplace=True) # Kalıcı değişiklik
print(df)

