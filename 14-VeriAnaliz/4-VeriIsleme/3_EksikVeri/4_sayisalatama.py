import numpy as np
import pandas as pd
from numpy.random import randn

arr = np.array([[10,15,np.nan],[25,np.nan,np.nan],[12,10,40]])
df = pd.DataFrame(arr,index=["Ocak","Şubat","Mart"],columns = ["Ankara","İstanbul","Adana"])

copy_df = df.copy()

print(df)
df = df.apply(lambda x: x.fillna(x.mean()) )
print(df) 
df = copy_df
df = df.fillna(df.mean()[:])
print(df)
df= copy_df
df = df.fillna(df.median()["Ankara":"İstanbul"])
print(df)
df = copy_df
df = df.where(pd.notna(df),df.mean(),axis=1 )
print(copy_df)
print(df)