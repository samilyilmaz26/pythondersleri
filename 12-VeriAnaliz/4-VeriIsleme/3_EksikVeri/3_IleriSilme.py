import numpy as np
import pandas as pd
from numpy.random import randn

arr = np.array([[10,15,np.nan],[np.nan,np.nan,np.nan],[28,10,40]])
df = pd.DataFrame(arr,index=["Ocak","Şubat","Mart"],columns = ["Ankara","İstanbul","Adana"])
 

print(df)
df = df.dropna(how="all") # Tüm satırları na olanle silinir
print(df)
df = df.dropna(axis=1) 
print(df)
df["Adana"] = np.nan
print(df )
df = df.dropna(how="all",axis=1 ,inplace=True)
print(df) 