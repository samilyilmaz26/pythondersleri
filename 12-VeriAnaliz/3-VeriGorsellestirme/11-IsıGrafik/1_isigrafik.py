import  seaborn as sea
fl  = sea.load_dataset("flights")
 
print(fl.head())
print(fl.shape)
print(fl["passengers"].describe().T) 
pv = fl.pivot("month","year","passengers")
print(pv)
print(sea.heatmap(pv))
