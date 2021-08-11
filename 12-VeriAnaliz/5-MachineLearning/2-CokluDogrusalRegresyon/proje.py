# statsmodels.formula.api

import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
import statsmodels.api as sm 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
import math as mt  
 
 
adv = pd.read_csv("Advertising.csv", usecols=[1,2,3,4])
print(adv.head())
 
 
X= adv.drop("sales", axis=1)
y= adv["sales"]
print(X[0:10])
X_train, X_test, y_train,y_test = train_test_split( X,y, test_size=0.20 ,random_state=42)
print(adv.shape)
print(X_train.shape)
print(X_test.shape)
train = adv.copy()
lm = sm.OLS(y_train,X_train)
model =  lm.fit()
print(model.summary())
print(model.summary().tables[1])

lm = LinearRegression()
model = lm.fit(X_train, y_train)
print(model.intercept_)
print(model.coef_)
# satis = 2.98 + TV*0.044 + radio*0.19 + newspaper*0.0027
# tv harcaması 30 radyao harcaması 10 gazete harcamısı 40 birim olan satış tahmini
yeni_veri = [[30],[10],[40]]
yeni_veri = pd.DataFrame(yeni_veri).T
print(yeni_veri)
satis = model.predict(yeni_veri)
print(satis)
rmse = mt.sqrt(mean_squared_error(y_train,model.predict(X_train)))# Best score 1.0 
print(rmse)
rmse2 = mt.sqrt(mean_squared_error(y_test,model.predict(X_test)))# Best score 1.0 
print(rmse2)
print(model.score(X_train,y_train))
#  Model  Doğrulama Tuning random_state=42 değiştirilir 
print(cross_val_score(model,X,y, cv = 10, scoring="r2").mean())
print(cross_val_score(model,X_train ,y_train , cv = 10, scoring="r2").mean())