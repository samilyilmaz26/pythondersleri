 
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
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
 

#Model
svr_model = SVR("rbf").fit(X_train, y_train)
y_pred = svr_model.predict(X_train)
 
print(y_pred[0:5])
 
y_pred = svr_model.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 
#Tune
svr_params = {"C": [0.1,0.5,1,3]}
svr_cv_model = GridSearchCV(svr_model,svr_params, cv = 5 ,verbose=2 ,n_jobs= -1).fit(X_train,y_train)
opt = svr_cv_model.best_params_
print(opt)
svr_tuned = SVR("linear", C= 0.5 ).fit(X_train,y_train)
y_pred = svr_tuned.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 

 