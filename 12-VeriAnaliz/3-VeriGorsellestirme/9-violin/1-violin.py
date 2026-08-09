import  seaborn as sea
tipsDf = sea.load_dataset("tips")
import matplotlib.pyplot as plt


print(sea.catplot(y= "total_bill",kind="violin", data=tipsDf))
plt.show()