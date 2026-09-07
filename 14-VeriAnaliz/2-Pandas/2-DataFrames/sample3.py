import numpy as np
import pandas as pd
from numpy.random import randn

matris =randn(3,3)
print (matris)
df = pd.DataFrame(randn(3,3)*10,index = ["S1","S2","S3"],columns = ["Ocak","Şubat","Mart"])
print(df)
print(df["Ocak"])
print(df.loc["S1"])
print(df[["Şubat","Mart"]])
df["Nisan "] = pd.Series(randn(3)*10,index = ["S1","S2","S3"]  )
print (df)
df["Toplam"] = df["Ocak"] + df["Şubat"] + df["Mart"]  
print (df)
#df.drop("Ocak"  ) #silemez
#print(df)
df.drop("Ocak" ,axis =1 , inplace=True)  
print(df)
