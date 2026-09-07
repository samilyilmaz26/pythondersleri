import  seaborn as sea
fm  = sea.load_dataset("fmri")
 
print(fm.head())
print(fm["timepoint"].describe().T)
print(fm["signal"].describe().T)
# print(fm.groupby("timepoint")["signal"].count())
print(fm.groupby("signal").count())
print(fm.groupby("timepoint")["signal"].describe())
