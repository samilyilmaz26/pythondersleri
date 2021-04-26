
import seaborn as sea
from pandas.api.types import CategoricalDtype #  ordinal tanımlama için
dia = sea.load_dataset("diamonds")
print(dia.head())
print(dia.info())
print(dia.describe().T)
print(dia["cut"].value_counts())
print(dia["color"].value_counts())
# ordinal tanımlama 
dia.cut = dia.cut.astype(CategoricalDtype(ordered=True))
print(dia.dtypes)
print(dia.cut.head(1))
cut_categories = ["Fair","Good","Very Good", "Premium","Ideal"]
dia.cut = dia.cut.astype(CategoricalDtype(categories = cut_categories , ordered=True))
print(dia.cut.head(1))
 
print(dia["cut"].value_counts().plot.barh().
      set_title("Cut değişkenleri"))

print(sea.barplot(x= "cut", y= dia.cut.index,data = dia))
