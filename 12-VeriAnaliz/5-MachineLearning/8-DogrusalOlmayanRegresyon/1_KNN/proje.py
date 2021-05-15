 
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import GridSearchCV
from warnings import filterwarnings

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

knn_model = KNeighborsRegressor().fit(X_train,y_train)

#Tahmin
y_pred = knn_model.predict(X_test)
 
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 

# mse_arr = []   anlatmak şart değil 
# for i in range(10):
#     i= i+1
#     knn_model = KNeighborsRegressor(n_neighbors=i).fit(X_train,y_train)
#     y_pred = knn_model.predict(X_train)
#     mse = np.sqrt(mean_squared_error(y_train,y_pred))
#     mse_arr.append(mse)
# print(mse_arr)

knn_params = {'n_neighbors': np.arange(1,30,1)}
knn = KNeighborsRegressor()
knn_cv_model = GridSearchCV(knn, knn_params, cv = 10)
knn_cv_model.fit(X_train, y_train)
opt = knn_cv_model.best_params_["n_neighbors"]
print(opt)
knn_tuned = KNeighborsRegressor(n_neighbors=opt)
knn_tuned.fit(X_train, y_train)
print(X_train)
y_pred = knn_tuned.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 
print(y_pred)



 

 
 
