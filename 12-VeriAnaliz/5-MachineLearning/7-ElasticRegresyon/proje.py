#%%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn.linear_model import ElasticNet,ElasticNetCV
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA  
from sklearn.preprocessing import scale
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
 
df = pd.read_csv("Hitters.csv")
print(df.head())
df =  df.dropna()
print(df.info())
print(df.describe().T)
d1 = df["League"]
dummies = pd.get_dummies(df[["League","Division","NewLeague"]])
print(dummies.head())
y = df["Salary"]
X_ = df.drop(["Salary","League" , "Division","NewLeague"], axis = 1).astype("float64")
print(X_.head())
X = pd.concat([X_ ,dummies[["League_N","Division_W","NewLeague_N"]]] ,axis=1)
print(X.head())
X_train, X_test, y_train,y_test = train_test_split( X,y, 
test_size=0.25 ,random_state=42)


enet_model = ElasticNet().fit(X_train, y_train)
print("coef",enet_model.coef_)
print("intercept",enet_model.intercept_)
y_pred = enet_model.predict(X_test)
print(y_pred)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 

#Tune
enet_cvmodel = ElasticNetCV(cv =10,random_state =0)
enet_cvmodel.fit(X_train, y_train)
opt = enet_cvmodel.alpha_
print(opt)
enet_tuned = ElasticNet(alpha=opt).fit(X_train, y_train)
enet_tuned.fit(X_train, y_train)
y_pred = enet_tuned.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred))) 
print("coef", enet_tuned.coef_)
print( "intercept", enet_model.intercept_)


 