#%%
import seaborn as sea
from pandas.api.types import CategoricalDtype #  ordinal tanımlama için
dia = sea.load_dataset("diamonds")
print(dia.head())
print(dia.info())
print(dia.describe().T)
print(dia["cut"].value_counts())
print(dia["color"].value_counts())
# ordinal tanımlama 
cut_categories = ["Fair","Good","Very Good", "Premium","Ideal"]
dia.cut = dia.cut.astype(CategoricalDtype(categories = cut_categories , ordered=True))
# print(dia.head(5))
#print(sea.catplot(x= "cut" , y= "price" , data = dia ))
print(sea.barplot(x= "cut", y= "price",hue = "color", data= dia ))
# print(dia.groupby(["cut","color"])["price"].mean())
# %%
