 
import seaborn as sns
import pandas as pd

df = sns.load_dataset("diamonds")
print(df.head())
print(df.describe().T)
print(df.dtypes)
print(df.isnull().values.any())
df = df.dropna()
df = df.select_dtypes(include = ["float64","int64"])
print(df.head())
df2 = df["table"]
print(df2.head())
print(sns.boxplot(x= df2))
Q1 = df2.quantile(0.25)
Q3 = df2.quantile(0.75)
IQR = Q3 -Q1
lowlimit = Q1-1.50*IQR
uplimit = Q3 + 1.50*IQR

print((df2<lowlimit) | (df2> uplimit) )

ar_extreme = (df2<lowlimit) | (df2> uplimit)
print(ar_extreme)
print(ar_extreme[0:10].index)

cleaned_df = df2[~ ((df2<lowlimit) | (df2> uplimit))]
print(df2.shape)
print(cleaned_df.shape)





 

 
