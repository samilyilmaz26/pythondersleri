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

# sns.histplot(df.Price ,kde ="False")
# sns.histplot(df.Price ,bins =50,kde ="False")
sns.histplot(df.Price, kde=True)

plt.show() 
#533 290 25 95 
#samilyilmaz@gmail.com 