import matplotlib.pyplot as plt
import seaborn as sea
dia = sea.load_dataset("diamonds")
 
#print(dia.head(5))
 
sea.catplot(x="cut", y="price", hue="color", kind="point", data=dia)
plt.show()
graph = sea.catplot(x="cut", y= "price", hue="color" ,kind="point" , data=dia)
# print(dia.describe().T)
graph.savefig("output.png")