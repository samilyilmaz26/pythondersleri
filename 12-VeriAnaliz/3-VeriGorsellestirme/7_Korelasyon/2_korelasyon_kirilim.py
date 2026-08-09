import  seaborn as sea 
import matplotlib.pyplot as plt
tipsDf = sea.load_dataset("tips")
sea.scatterplot(x= "total_bill", y= "tip",hue="time" ,data = tipsDf)
plt.show()
sea.scatterplot(x= "total_bill", y= "tip",hue="time",style="time" ,data = tipsDf)
plt.show()
sea.scatterplot(x= "total_bill", y= "tip",hue="day",style="day" ,data = tipsDf)
plt.show()
sea.scatterplot(x= "total_bill", y= "tip",hue="size",size="size" ,data = tipsDf)
plt.show()
sea.scatterplot(x= "total_bill", y= "tip",size="size" ,data = tipsDf)
plt.show()