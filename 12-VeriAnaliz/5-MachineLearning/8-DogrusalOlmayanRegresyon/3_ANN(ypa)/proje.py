 
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



#Model
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
scaler.fit(X_test)
X_test_scaled = scaler.transform(X_test)

ypa_model = MLPRegressor().fit(X_train_scaled,y_train)
y_pred = ypa_model.predict(X_test_scaled)
print(y_pred[0:5])
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 

  
#Tune 

ypa_params = { "alpha": [0.1, 0.01,0.02,0.005], 
"hidden_layer_sizes": [(10,20), (5,5),(100,100)]}
ypa_cv_model = GridSearchCV(ypa_model,ypa_params,
 cv= 10 , verbose = 2 ,n_jobs=-1).fit(X_train,y_train)

opt = ypa_cv_model.best_params_
print(opt)
ypa_tuned =  mlp_tuned = MLPRegressor(alpha = 0.005, hidden_layer_sizes = 
(100,100)).fit(X_train_scaled, y_train) 
y_pred = ypa_tuned.predict(X_test_scaled)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 




 




 



 