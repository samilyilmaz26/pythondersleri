import seaborn as sea
from pandas.api.types import CategoricalDtype #  ordinal tanımlama için
dia = sea.load_dataset("diamonds")
 
# ordinal tanımlama 
cut_categories = ["Fair","Good","Very Good", "Premium","Ideal"]
dia.cut = dia.cut.astype(CategoricalDtype(categories = cut_categories , ordered=True))
print(dia.head(5))
# #print(sea.FacetGrid(dia,
#                     hue ="cut",
#                     height=5,
#                     xlim=(0,10000))
#       .map(sea.kdeplot, "price",shade=True).add_legend()
#       )
print(sea.catplot(x="cut", y= "price", hue="color" ,kind="point" , data=dia))
graph = sea.catplot(x="cut", y= "price", hue="color" ,kind="point" , data=dia)
print(dia.describe().T)
graph.savefig("output.png")

