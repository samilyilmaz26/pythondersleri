import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("telecom_users.csv")
print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())
# df.fillna(0,inplace=True)
# print(df.isnull().values.sum())

sns.histplot(df.MonthlyCharges ,kde ="true" ,bins =50)
plt.show()

# # print(sns.distplot(df.Price ,bins =50,kde ="False"))
# # print(sns.distplot(df.Price ,hist = False)) 
