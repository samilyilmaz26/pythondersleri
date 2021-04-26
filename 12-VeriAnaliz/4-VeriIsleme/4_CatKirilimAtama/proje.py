import numpy as np 
import pandas as pd

S1 = np.array  ([10000,3000,6000,np.nan,3000,1500,np.nan,9500,1580])
S2 = np.array  ([7,np.nan,5,8,12,np.nan,np.nan,2,3])
S3 = np.array  ([np.nan,12,5,6,14,7,np.nan,2,31])
S4 = np.array  (["BT","BT","IK","IK","IK","IK","BT","BT","BT"])
df = pd.DataFrame(
    {
       "Maas" : S1, 
        "S2" : S2,
        "S3" : S3,
        "Dep" : S4
    }
)
print(df )
print(df.groupby("Dep")["Maas"].mean())
 
df =  (df["Maas"].fillna(df.groupby("Dep")["Maas"].transform("mean"))) 
print(df)
 