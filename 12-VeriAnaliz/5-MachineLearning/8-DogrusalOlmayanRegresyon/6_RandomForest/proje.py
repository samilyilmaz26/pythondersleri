 
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
from sklearn.ensemble import RandomForestRegressor
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

#Tahmin
rf_model = RandomForestRegressor(random_state=42).fit(X_train,y_train)
y_pred = rf_model.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 
# Tune
rf_params = {'max_depth' : list(range(1,10)),
             'max_features': [3,5,10,15],
             'n_estimators': [100,200,500,1000,2000]

}
rf_model = RandomForestRegressor(random_state=42)
rf_cv_model = GridSearchCV(rf_model,rf_params ,cv=10,n_jobs= -1).fit(X_train,y_train)
print(rf_cv_model.best_params_)
rf_tuned_model = RandomForestRegressor(max_depth= 8,
 n_estimators=100, max_features = 3).fit(X_train,y_train)
y_pred = rf_tuned_model.predict(X_test)

print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 
 
 
