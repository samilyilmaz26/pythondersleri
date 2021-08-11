# statsmodels.formula.api

import pandas as pd
import seaborn as sea
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sklearn.linear_model as sk 

adv = pd.read_csv("Advertising.csv")
print(adv.head())
adv = adv.iloc[:,1:len(adv)]
print(adv.head())
print(adv.info())
print(adv.describe().T)
print(adv.isnull().any())
print(adv.corr())
print(sea.pairplot(adv,kind="reg"))
print(sea.jointplot(x="TV",y="sales",data= adv ,kind="reg"))
# istatiksel model
X= adv[["TV"]]
print(X[0:5])
X = sm.add_constant(X)
y = adv["sales"]
linmodel2 = sm.OLS(y,X)
linmodel = smf.ols("sales ~ TV", adv)
model =linmodel.fit()
print(model.summary())
print(model.params)
print(model.fittedvalues[0:5])
print(y[0:5])
# statsmodels.formula.api as smf
print("Sales" + str("%.2f" %model.params[0]) + " + TV"  +     " * " + str("%.2f" %model.params[1]) )
def CalculateSales(tvExpense) :
    return 7.03 + tvExpense*0.05
    

print(CalculateSales(30))

