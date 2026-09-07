import  seaborn as sea
tipsDf = sea.load_dataset("tips")
print(tipsDf.head())
print(tipsDf.dtypes)
print(tipsDf.shape)
print(sea.pairplot(tipsDf,hue="sex") )
print(sea.pairplot(tipsDf,hue="sex", kind="reg") )
