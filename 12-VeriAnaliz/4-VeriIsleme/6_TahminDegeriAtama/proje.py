#pip install ycimpute
#KKN tahmine Dayalı Yöntem
import  seaborn as sns
import missingno as msno
import numpy as np
import pandas as pd
from ycimpute.imputer import knnimput #nearest

df = sns.load_dataset("titanic")
df = df.select_dtypes(include =["float64","int64"])
print(df)
print(df.isnull().sum())
var_name = list(df)
print(var_name)
arr_df = np.array(df)
print(arr_df)
print(arr_df.shape)

arr_dffill = knnimput.KNN(k= 4).complete(arr_df)
print(arr_dffill)
df_fill = pd.DataFrame(arr_dffill,columns=var_name)
print(df_fill.isnull().sum())
