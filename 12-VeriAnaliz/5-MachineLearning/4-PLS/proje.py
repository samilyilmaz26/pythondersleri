import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict
from sklearn.cross_decomposition import PLSRegression,PLSSVD
#import statsmodels.api as sm 
from sklearn.linear_model import LinearRegression 
#from sklearn.metrics import mean_squared_error
#import math as mt  
  
from sklearn.preprocessing import scale
 
df = pd.read_csv("Hitters.csv")
print(df.head())
df =  df.dropna()
print(df.head())
print(df.info())
print(df.describe().T)
dummies = pd.get_dummies(df[["League","Division","NewLeague"]])
print(dummies.head())
y= df["Salary"]
print(y)
X_ = df.drop(["League" , "Division","NewLeague"], axis = 1).astype("float64")
print(X_.head())
X = pd.concat([X_ ,dummies[["League_N","Division_W","NewLeague_N"]]] ,axis=1)
print(X.head())
X_train, X_test, y_train,y_test = train_test_split( X,
y, test_size=0.20 ,random_state=42)
training = df.copy()
print("X_train",X_train.shape)
print("y_train",y_train.shape)
print("X_test",X_test.shape)
print("y_test",y_test.shape)
print("training ",training.shape)

# pls_model = PLSRegression().fit(X_train,y_train)
# # print(pls_model.coef_)  
# pls_model = PLSRegression(n_components=2).fit(X_train,y_train)
# # print(pls_model.coef_) 
# print(pls_model.predict(X_train))
# print(X_train.head())