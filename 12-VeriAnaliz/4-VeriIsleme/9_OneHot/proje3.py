import pandas as pd
import numpy as np
import  seaborn as sns
 

df = sns.load_dataset("tips")
print(df)
df_oneHot = pd.get_dummies(df , columns=["day"],prefix="day")
print(df_oneHot)
 