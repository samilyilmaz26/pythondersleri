import  seaborn as sea
import matplotlib.pyplot as plt


tipsDf = sea.load_dataset("tips")
print(tipsDf.describe().T)
#hangi gün daha çok kazanç
#print(sea.boxplot(x= "day", y= "total_bill",data=tipsDf))
#hangi öğün  daha çok kazanç
#print(sea.boxplot(x= "time", y= "total_bill",data=tipsDf))
# #Kişi Sayısı Kazanç ilişkisi
#print(sea.boxplot(x= "size", y= "total_bill",data=tipsDf))
print(sea.boxplot(x= "day", y= "total_bill",hue="sex",data=tipsDf))
plt.show()