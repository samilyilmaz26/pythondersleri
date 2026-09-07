import  seaborn as sea
import matplotlib.pyplot as plt
tipsDf = sea.load_dataset("tips")
sea.scatterplot(x= "total_bill", y= "tip", data = tipsDf)
plt.show()