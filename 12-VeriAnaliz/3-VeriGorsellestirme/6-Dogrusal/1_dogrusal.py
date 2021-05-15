#%%
import  seaborn as sea
import  matplotlib.pyplot as plt

tipsDf = sea.load_dataset("tips")
print(sea.lmplot (x= "total_bill", y= "tip", data = tipsDf))
print(sea.lmplot (x= "total_bill", y= "tip", hue='smoker',  data = tipsDf))
print(sea.lmplot (x= "total_bill", y= "tip", hue='smoker',col="time" ,  data = tipsDf))
print(sea.lmplot (x= "total_bill", y= "tip", hue='smoker',
                  col="time" ,row = "sex", data = tipsDf))


# %%
