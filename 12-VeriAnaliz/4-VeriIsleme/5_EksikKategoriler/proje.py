import numpy as np 
import pandas as pd

S1 = np.array  ([10000,3000,6000,np.nan,3000,1500,np.nan,9500,1580])
 
S4 = np.array  (["BT", np.nan,"IK","IK","IK","IK","BT","BT","IK"],dtype=object)
df = pd.DataFrame(
    {
       "Maas" : S1, 
        
        "Dep" : S4
    }
)
df_copy = df.copy()
df_copy2 = df.copy()
print(df )
print(df["Dep"].mode()[0])
df["Dep"].fillna(df["Dep"].mode()[0],inplace=True)
print(df)

df = df_copy
print(df)
df["Dep"].fillna(method="bfill",inplace=True)
print(df)

df = df_copy2
print(df)
df["Dep"].fillna(method="ffill",inplace=True)
print(df)
 
 
 
 
 
 
 