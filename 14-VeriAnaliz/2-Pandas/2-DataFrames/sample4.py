import numpy as np
import pandas as pd
from numpy.random import randn

matris =randn(3,3)
print (matris)
df = pd.DataFrame(randn(3,3)*10,index = ["S1","S2","S3"],columns = ["Ocak","Şubat","Mart"])
print(df)
print(df[["Ocak","Şubat"]])
print(df.loc["S1"])
print(df.iloc[1] )# 1.index yani S2
print(df.loc["S1","Ocak"])
print(df.loc[["S1","S2"],["Ocak","Şubat"]])
