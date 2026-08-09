import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("melb_data.csv")

print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())


print(df.isnull().values.sum())
#sns.catplot(x= "Type",y= "Price",data=df)
#sns.barplot(x= "Type",y="Price",hue ="Regionname",data = df)

# sns.barplot(x= "Type",y="Price",hue ="Method" ,data = df)
# sns.catplot(x= "Method",y= "Price",data=df)
# sns.catplot(x= "Method",y= "Price",hue="Regionname",data=df)
# sns.catplot(x= "Regionname",y= "Price",data=df)
sns.catplot(x= "Regionname",y= "Price",hue="Type",data=df)

plt.show()




 

