import  seaborn as sea
import matplotlib.pyplot as plt
tipsDf = sea.load_dataset("tips")

#print(sea.catplot(x= "day",y= "total_bill",kind="violin",  data=tipsDf))
sea.catplot(x= "day",y= "total_bill",kind="violin", hue="smoker", data=tipsDf)
plt.show()
