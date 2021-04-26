 
import seaborn as sns
import pandas as pd

df = sns.load_dataset("diamonds")
 
df = df.select_dtypes(include= ["float64","int64"])
df = df.dropna()
 
df_table = df["table"]
sns.boxplot(x= df_table)
Q1 = df_table.quantile(0.25)
Q3 = df_table.quantile(0.75)
IQR = Q3-Q1
lowlimit = Q1-1.5*IQR
uplimit = Q3+ 1.5*IQR
ar_low = df_table<lowlimit
print(df_table[ar_low]) 
print(df_table.mean())
df_table[ar_low]   = df_table.mean()
print(df_table[ar_low])  
print(df_table.mean()) 
df_table = pd.DataFrame(df_table)
 