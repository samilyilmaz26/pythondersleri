import seaborn as sea
import matplotlib.pyplot as plt
#from pandas.api.types import CategoricalDtype #  ordinal tanımlama için
dia = sea.load_dataset("diamonds")
 
# ordinal tanımlama 
#cut_categories = ["Fair","Good","Very Good", "Premium","Ideal"]
#dia.cut = dia.cut.astype(CategoricalDtype(categories = cut_categories , ordered=True))
print(dia.head(5))
#sea.histplot(dia.price ,kde= True  )


#sea.histplot(dia.price ,bins = 10,kde= False)
import seaborn as sns

sea.histplot(dia.price, kde=True, element="poly", fill=False)

# print(dia["price"].describe())
plt.show()