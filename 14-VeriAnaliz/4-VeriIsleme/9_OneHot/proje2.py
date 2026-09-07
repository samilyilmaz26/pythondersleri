import pandas as pd
import numpy as np
import  seaborn as sns
from sklearn.preprocessing import LabelEncoder

df = sns.load_dataset("tips")
print(df)
df_oneHot = pd.get_dummies(df , columns=["sex"],prefix="sex")
print(df_oneHot)
df_oneHot.drop("sex_Female",axis=1,inplace=True)
print(df_oneHot)