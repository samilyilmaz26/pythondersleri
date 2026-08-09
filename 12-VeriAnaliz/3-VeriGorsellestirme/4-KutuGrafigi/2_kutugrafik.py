
import  seaborn as sea
tipsDf = sea.load_dataset("tips")
import matplotlib.pyplot as plt

# print(sea.boxplot(x= tipsDf["total_bill"]))

print(sea.boxplot(x= tipsDf["total_bill"],orient="v"))

plt.show()