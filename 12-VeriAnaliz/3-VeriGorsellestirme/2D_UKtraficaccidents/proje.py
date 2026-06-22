#%%

import  numpy as np
import pandas as pd
import seaborn as sns


df = pd.read_csv("accidents.csv")

print(df)


print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())
print(df["Speed_limit"])

# print( sns.catplot(x= "Type",y= "Price",data=df))
# print (sns.barplot(x= "Type",y="Price",
# hue ="Regionname",data = df))
# print (sns.barplot(x= "Type",y="Price",hue ="Method" ,data = df))
# print( sns.catplot(x= "Method",y= "Price",data=df))
# print( sns.catplot(x= "Method",y= "Price",hue="Regionname",data=df))
# print( sns.catplot(x= "Regionname",y= "Price",data=df))
# print( sns.catplot(x= "Regionname",y= "Price",hue="Type",data=df))
# print(sns.catplot(x= "Accident_Severity", y="Speed_limit",data=df))
#print(sns.barplot(x= "Accident_Severity", y="Speed_limit",data=df))print(sns.catplot(x= "Type", y="Price", hue="Method" , kind="point",data=df))
# print(sns.barplot(x= "Accident_Severity", y="Number_of_Vehicles",data=df))
# print(sns.barplot(x= "Police_Force", hue="Accident_Severity",y="Speed_limit",data=df))
# print(sns.catplot(x= "Police_Force" , hue="Accident_Severity",y="Speed_limit",data=df))
print(sns.catplot(x= "Weather_Conditions" , y="Number_of_Casualties",data=df))
print(sns.catplot(x= "Road_Surface_Conditions" , y="Number_of_Casualties",data=df))
print(sns.catplot(x= "Light_Conditions" , y="Number_of_Casualties",data=df))
print(sns.catplot(x= "Special_Conditions_at_Site" , y="Number_of_Casualties",data=df))
print(sns.catplot(x= "Carriageway_Hazards" , y="Number_of_Casualties",data=df))
print(sns.catplot(x= "Carriageway_Hazards" ,hue="Weather_Conditions", y="Number_of_Casualties",data=df))
# %%
