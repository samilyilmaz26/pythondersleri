import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("melb_data.csv")
print(df)
print(df.info())
print(df.dtypes)
print(df.isnull().values.any())
print(df.isnull().values.sum())

# numeric_cols = df.select_dtypes(include=["number"]).columns
# object_cols = df.select_dtypes(include=["object"]).columns

# if len(numeric_cols) > 0:
#     df[numeric_cols] = df[numeric_cols].fillna(0)
# if len(object_cols) > 0:
#     df[object_cols] = df[object_cols].fillna("Unknown")

# print(df.isnull().values.sum())

print(sns.catplot(x= "Type", y="Price", hue="Method" , kind="point",data=df))
print(sns.catplot(x= "YearBuilt", y="Price", hue="CouncilArea" , kind="point",data=df))
plt.show()
 