import  seaborn as sea
tipsDf = sea.load_dataset("tips")

print(sea.catplot(y= "total_bill",kind="violin", data=tipsDf))
