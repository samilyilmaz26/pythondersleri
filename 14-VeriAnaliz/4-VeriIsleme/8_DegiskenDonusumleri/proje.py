import pandas as pd
import numpy as np
import  seaborn as sns
from sklearn.preprocessing import LabelEncoder

df = sns.load_dataset("tips")
print(df)
lb = LabelEncoder() 
print(lb.fit_transform(df["sex"]))
df["new_sex"] = lb.fit_transform(df["sex"])
df["new_day"] = np.where(df["day"].str.contains("Sun"),1 ,0)
df["new_day2"] = np.where((df["day"].str.contains("Sun")) |
(df["day"].str.contains("Sat"))   ,1 ,0)
print(df)
print(lb.fit_transform(df["day"])) # bu durumda one-hot dönüşümü 
