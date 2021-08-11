import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
from sklearn.cross_decomposition import PLSRegression,PLSSVD
from sklearn.preprocessing import scale
from sklearn.metrics import r2_score
 
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
print(df.shape)
print(X_train.shape)
print(X_test.shape)

#pls_model = PLSRegression().fit(X_train, y_train)
pls_model = PLSRegression(n_components=2).fit(X_train, y_train)
#print(pls_model.coef_)
y_pred = pls_model.predict(X_train)
print(np.sqrt(mean_squared_error(y_train,y_pred)))  
print(r2_score(y_train,y_pred)) # Best score 1.0

y_pred = pls_model.predict(X_test)
print(np.sqrt(mean_squared_error(y_test,y_pred)))  
print(r2_score(y_test,y_pred)) # Best score 1.0

