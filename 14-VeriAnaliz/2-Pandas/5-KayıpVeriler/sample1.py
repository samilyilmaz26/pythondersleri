import numpy as np
import pandas as pd
from numpy.random import randn

arr = np.array([[10,20,np.nan],[5,15,np.nan],[28,10,40]])
df = pd.DataFrame(arr,index=["Ocak","Şubat","Mart"],columns = ["Ankara","İstanbul","Adana"])
print(df)
print(df.dropna())
print(df.dropna(axis = 1))
 
print(df.dropna(thresh = 3))  
print(df.fillna(value = 0))
print(df.sum())
print(df.sum().sum())