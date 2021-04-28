 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn.linear_model import Lasso,LassoCV
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
print(df.shape)
print(X_train.shape)
print(X_test.shape)

#Tune
lasso_cv_model = LassoCV(alphas=None,cv =10 ,max_iter=10000 ,normalize =True)
lasso_cv_model.fit(X_train, y_train)
opt = lasso_cv_model.alpha_
print(opt)

#Tune
lasso_tuned = Lasso(alpha=opt)
lasso_tuned.fit(X_train,y_train)
y_pred = lasso_tuned.predict(X_test)
print("mse" ,np.sqrt(mean_squared_error(y_test,y_pred)))  
print("r2",r2_score(y_test,y_pred)) # Best score 1.0 