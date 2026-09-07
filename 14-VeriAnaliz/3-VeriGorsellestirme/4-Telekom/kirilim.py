
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



df = pd.read_csv("telecom_users.csv")
 
 
# print( sns.barplot(x= "StreamingTV",hue="Partner",y= "MonthlyCharges",data=df))
# print( sns.barplot(x= "StreamingTV",hue="SeniorCitizen",y= "MonthlyCharges",data=df))
# print( sns.barplot(x= "StreamingTV",hue="gender",y= "MonthlyCharges",data=df))
# print( sns.barplot(x= "Dependents",hue="gender",y= "MonthlyCharges",data=df))
print( sns.barplot(x= "StreamingTV",hue="Dependents",y= "MonthlyCharges",data=df))
plt.show()
 

