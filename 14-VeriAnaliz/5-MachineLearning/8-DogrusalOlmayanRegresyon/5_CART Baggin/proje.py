 
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
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import BaggingRegressor
from warnings import filterwarnings

df = pd.read_csv("Hitters.csv")
print(df.head())
df =  df.dropna()
print(df.info())
print(df.describe().T)
 
dummies = pd.get_dummies(df[["League","Division","NewLeague"]])
print(dummies.head())
y = df["Salary"]
X_ = df.drop(["Salary","League" , "Division","NewLeague"], axis = 1).astype("float64")
print(X_.head())
X = pd.concat([X_ ,dummies[["League_N","Division_W","NewLeague_N"]]] ,axis=1)
print(X.head())
X_train, X_test, y_train,y_test = train_test_split( X,y, 
test_size=0.25 ,random_state=42)

bag_model  = BaggingRegressor(bootstrap_features=True)
bag_model =  bag_model.fit(X_train, y_train)
print(bag_model.n_estimators)
print(bag_model.estimators_)
print(bag_model.estimators_samples_)
print(bag_model.estimators_features_)

# Tahmin
y_pred =  bag_model.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 

second_y_pred = bag_model.estimators_[1].fit(X_train, y_train).predict(X_test)
print("mseSecond" ,np.sqrt(mean_squared_error(y_test,second_y_pred   )))  
print("r2Sec",r2_score(y_test, second_y_pred)) # Best score 1.0 
 
 #Tune
bag_params = {"n_estimators": range (2,20)}
bag_cv_model = GridSearchCV(bag_model ,bag_params,cv =10)
bag_cv_model = bag_cv_model.fit(X_train, y_train)
print(bag_cv_model.best_params_)
bag_tuned = BaggingRegressor(n_estimators=12, random_state=42)
bag_tuned = bag_tuned.fit(X_train, y_train)
y_pred = bag_tuned.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 