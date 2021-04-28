import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA  
from sklearn.preprocessing import scale
from sklearn.metrics import r2_score
 
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
training = df.copy()
print("training",training.shape)
 
pca = PCA()
X_reduced_train = pca.fit_transform(scale(X_train)) #fit transform hem fit hemde indirgeme yapar
print(X_reduced_train[0:1,:])
print(np.cumsum(np.round(pca.explained_variance_ratio_,decimals=4)*100)[0:6]) #19 ile 6 gir
lm = LinearRegression()
pcr_model = lm.fit(X_reduced_train,y_train)
print(pcr_model.intercept_)
print(pcr_model.coef_)



#     Tahmin 
y_pred = pcr_model.predict(X_reduced_train)
print(y_pred [0:6])
print(np.sqrt(mean_squared_error(y_train,y_pred)))  #google da bul anlat
print(df["Salary"].mean()) 
print(r2_score(y_train,y_pred)) # Best score 1.0

pca_test = PCA()
X_reduced_test = pca_test.fit_transform(scale(X_test)) #fit transform hem fit hemde indirgeme yapar
y_pred_t = pcr_model.predict(  X_reduced_test)
print( "mse", np.sqrt(mean_squared_error(y_test,y_pred_t)))  

# Degişken Sınırlama ile Tahmin
lm = LinearRegression()
pcr_model = lm.fit(X_reduced_train[:,0:6],y_train)
print(pcr_model.intercept_)
print(pcr_model.coef_)
y_pred_t = pcr_model.predict(X_reduced_test[0:,0:6])
print( "mse", np.sqrt(mean_squared_error(y_test,y_pred_t))) #anlatma

