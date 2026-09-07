import numpy as np
import pandas as pd
from numpy.random import randn

arr = np.array([[10,15,np.nan],[5,np.nan,np.nan],[28,10,40]])
df = pd.DataFrame(arr,index=["Ocak","Şubat","Mart"],columns = ["Ankara","İstanbul","Adana"])
print(df)
print(df.isnull().sum())
print(df.notnull().sum())
print(df.isnull().sum().sum())
print(df.isnull())
print(df[df.isnull().any(axis =1)] )
print(df[df.notnull().all(axis =1)])
df = df.dropna(inplace=True)
print (df["İstanbul"].mean())
df["İstanbul"] = df["İstanbul"].fillna(df["İstanbul"].mean()) 
print(df["İstanbul"])
df = df.apply(lambda x: x.fillna(x.mean()) )
print(df)
