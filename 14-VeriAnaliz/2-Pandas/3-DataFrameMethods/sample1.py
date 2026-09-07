import numpy as np
import pandas as pd
from numpy.random import randn
 
df = pd.DataFrame(randn(3,3)*10,index = ["S1","S2","S3"],columns = ["Ocak","Şubat","Mart"])
print(df)
print(df> 1)
df2 = df> 1
print(df2)
print(df[df2])
print(df["Şubat"])
print(df[df["Şubat"] > -1])
print(df[df["Şubat"] <0])
print(df2["Şubat"]<0)
print(df["Mart"] < 0)
print(df[df["Mart"] < 0])
print(df[(df["Ocak"] > -1) & (df["Mart"] > 0)])

