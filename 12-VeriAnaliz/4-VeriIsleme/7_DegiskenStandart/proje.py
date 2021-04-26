import pandas as pd
import numpy as np
from sklearn import preprocessing

V1 = np.array([1,3,6,5,7])
V2 = np.array([7,7,5,9,12])
V3 = np.array([6,12,5,6,14])
 
df = pd.DataFrame({
    "V1":V1,
    "V2":V2,
    "V3":V3
})
df = df.astype(float)
print(df)
print(preprocessing.scale(df))
normal = preprocessing.normalize(df)
 
print(normal) 
minmax = preprocessing.MinMaxScaler(feature_range=(0,50)).fit_transform(df)
print(minmax)
print(df.describe().T)
 

