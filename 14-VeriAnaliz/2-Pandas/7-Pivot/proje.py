import pandas as pd
import numpy  as np
df = pd.DataFrame({
    "Col1":[1,2,3,4,5,6],
    "Col2":[100,100,200,300,300,100],
    "Col3":["Şamil","Kamil","Ali","Ayşe","Murat","Zeynep"]
    })
print(df)
print(df.head())
print(df.head(3))
print(df["Col2"].unique())
print(df["Col2"].nunique())
print(df["Col2"].value_counts())
print(df[df["Col1"]>= 4])
print(df["Col2"].apply(lambda x: x*2))
print(df.drop("Col3",axis = 1, inplace=False))
print(df.columns)
print(df.index)
print(len(df.index))
print(df.sort_values("Col2",ascending = False))
