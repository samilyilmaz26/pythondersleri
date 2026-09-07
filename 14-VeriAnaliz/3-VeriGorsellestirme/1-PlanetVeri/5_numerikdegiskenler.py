import seaborn as sea
import pandas as pd
pl = sea.load_dataset("planets")
num_df  = pl.select_dtypes(include =["float64","int64"])
print(num_df)
print(num_df.describe())
print(num_df.describe().T)
print(num_df["distance"].describe())