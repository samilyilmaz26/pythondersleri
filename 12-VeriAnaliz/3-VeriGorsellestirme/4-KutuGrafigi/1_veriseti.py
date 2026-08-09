import  seaborn as sea
tipsDf = sea.load_dataset("tips")
print("hi")
print(tipsDf.head())
print(tipsDf.describe().T)
print(tipsDf["smoker"].value_counts())
print(tipsDf["day"].value_counts())
print(tipsDf["tip"].mean())
