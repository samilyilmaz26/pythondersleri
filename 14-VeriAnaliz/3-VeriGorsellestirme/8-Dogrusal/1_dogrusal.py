
import  seaborn as sea
import  matplotlib.pyplot as plt

tipsDf = sea.load_dataset("tips")
# sea.lmplot (x= "total_bill", y= "tip", data = tipsDf)
sea.lmplot (x= "total_bill", y= "tip", hue='smoker',  data = tipsDf)
# sea.lmplot (x= "total_bill", y= "tip", hue='smoker',col="time" ,  data = tipsDf)
# sea.lmplot (x= "total_bill", y= "tip", hue='smoker', 
          #  col="time" ,row = "sex", data = tipsDf)
plt.show()
