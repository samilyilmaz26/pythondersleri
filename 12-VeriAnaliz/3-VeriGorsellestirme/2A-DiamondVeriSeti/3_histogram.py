import seaborn as sea
from pandas.api.types import CategoricalDtype #  ordinal tanımlama için
dia = sea.load_dataset("diamonds")
 
# ordinal tanımlama 
cut_categories = ["Fair","Good","Very Good", "Premium","Ideal"]
dia.cut = dia.cut.astype(CategoricalDtype(categories = cut_categories , ordered=True))
print(dia.head(5))
print(sea.distplot(dia.price ,kde= False  ))
print(sea.distplot(dia.price ,bins = 10,kde= False))
print(sea.distplot(dia.price ,hist = False))
print(dia["price"].describe())