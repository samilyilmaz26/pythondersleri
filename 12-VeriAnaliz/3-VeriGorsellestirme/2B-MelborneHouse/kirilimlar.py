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
print( sns.catplot(x= "Type",y= "Price",data=df))
print (sns.barplot(x= "Type",y="Price",hue ="Regionname",data = df))
print (sns.barplot(x= "Type",y="Price",hue ="Method" ,data = df))
print( sns.catplot(x= "Method",y= "Price",data=df))
print( sns.catplot(x= "Method",y= "Price",hue="Regionname",data=df))
print( sns.catplot(x= "Regionname",y= "Price",data=df))
print( sns.catplot(x= "Regionname",y= "Price",hue="Type",data=df))
 
 

