#%%
import pandas as pd
import seaborn as sns

df = pd.read_csv("telecom_users.csv")
print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())
df = df.dropna() 

print(sns.catplot(x= "StreamingTV", y="MonthlyCharges", hue="Partner" , kind="point",data=df))
 
# %%
