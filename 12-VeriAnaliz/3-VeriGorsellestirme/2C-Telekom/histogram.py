import pandas as pd
import seaborn as sns

df = pd.read_csv("telecom_users.csv")
print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())
df.fillna(0,inplace=True)
print(df.isnull().values.sum())

print(sns.distplot(df.Price ,kde ="False"))
print(sns.distplot(df.Price ,bins =50,kde ="False"))
print(sns.distplot(df.Price ,hist = False)) 

