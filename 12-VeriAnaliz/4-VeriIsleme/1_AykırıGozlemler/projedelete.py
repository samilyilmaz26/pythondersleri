#%%
import seaborn as sns
import pandas as pd

df = sns.load_dataset("diamonds")
print(df)
df = df.select_dtypes(include= ["float64","int64"])
df = df.dropna()
print(df) 
df_table = df["table"]
sns.boxplot(x= df_table)
Q1 = df_table.quantile(0.25)
Q3 = df_table.quantile(0.75)
IQR = Q3-Q1
lowlimit = Q1-1.5*IQR
uplimit = Q3+ 1.5*IQR
print(df_table<lowlimit)
print(df_table>uplimit)
print((df_table<lowlimit) | (df_table>uplimit))
ar_extreme = (df_table<lowlimit) | (df_table>uplimit)
ar_low = df_table<lowlimit
print(ar_extreme)
print(df_table[ar_extreme])
print(df_table[ar_extreme].index)

#  Silme
df_table = pd.DataFrame(df_table)
print(df_table.shape)
cleaned_df = df_table[~((df_table<lowlimit) | (df_table > uplimit)).any(axis=1) ]
print(cleaned_df)

# %%
