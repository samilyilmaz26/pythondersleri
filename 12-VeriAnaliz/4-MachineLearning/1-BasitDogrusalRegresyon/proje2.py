# sklearn Model 

import pandas as pd
import seaborn as sea
from sklearn.linear_model import LinearRegression
 

adv = pd.read_csv("Advertising.csv")
print(adv.head())
adv = adv.iloc[:,1:len(adv)]
print(adv.head())
print(adv.info())
print(adv.describe().T)
print(adv.isnull().any())
print(adv.corr())
print(sea.pairplot(adv,kind="reg"))
print(sea.jointplot(x="TV",y="sales",data= adv ,kind="reg"))
# sklearn Model 
X = adv[["TV"]]
y = adv["sales"]
reg = LinearRegression()
model = reg.fit(X,y)
print(model.intercept_ )
print(model.coef_)
print(model.score(X,y)) # R kare değeri
print(model.predict(X) [0:10])
print(model.predict([[30]]))
ucdeger = [[30],[200],[3000]]
print (model.predict(ucdeger))


 

 
 

