import pandas as pd
import seaborn as sns

df = pd.read_csv("melb_data.csv")
print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())
df.fillna(0,inplace=True)
print(df.isnull().values.sum())

print(sns.catplot(x= "Type", y="Price", hue="Method" , kind="point",data=df))
 