import seaborn as sea
import pandas as pd
pl = sea.load_dataset("planets")
kat_df  = pl.select_dtypes(include =["object"])
# print(kat_df)
print(kat_df.method.unique())
# print(kat_df["method"].value_counts().count())
# print(kat_df["method"].value_counts())
# print(pl["method"].value_counts().plot.barh())