 
import seaborn as sns
import  pandas as pd
df = sns.load_dataset("diamonds")
df = df.dropna()

df2 = df["table"]
print(sns.boxplot(x= df2)) 
Q1 = df2.quantile(0.25)
Q3 = df2.quantile(0.75)
IQR = Q3-Q1
lowlimit = Q1-1.5*IQR
uplimit = Q3+1.5*IQR

ar_low = df2<lowlimit
print(df2[ar_low])
print(df2.mean())
df2[ar_low] = df2.mean()
print(df2[ar_low])
print(df2.mean())

