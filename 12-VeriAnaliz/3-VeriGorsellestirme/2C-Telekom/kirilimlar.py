#%%
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
# print( sns.catplot(x= "StreamingTV",y= "MonthlyCharges",data=df))
# print( sns.catplot(x= "StreamingTV",hue="Partner",y= "MonthlyCharges",data=df))
# print( sns.barplot(x= "StreamingTV",hue="Partner",y= "MonthlyCharges",data=df))
# print( sns.barplot(x= "StreamingTV",hue="SeniorCitizen",y= "MonthlyCharges",data=df))
#print( sns.barplot(x= "StreamingTV",hue="gender",y= "MonthlyCharges",data=df))
print( sns.barplot(x= "Dependents",hue="gender",y= "MonthlyCharges",data=df))
print( sns.barplot(x= "StreamingTV",hue="Dependents",y= "MonthlyCharges",data=df))
 
 
 


# %%
