 
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor 

df = sns.load_dataset("diamonds")
 
df = df.select_dtypes(include= ["float64","int64"])
df = df.dropna()
clf = LocalOutlierFactor(n_neighbors=20 ,contamination=0.1)
print(clf.fit_predict(df))
df_scores = clf.negative_outlier_factor_
 
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor 

df = sns.load_dataset("diamonds")
 
df = df.select_dtypes(include= ["float64","int64"])
df = df.dropna()
clf = LocalOutlierFactor(n_neighbors=20 ,contamination=0.1)
print(clf.fit_predict(df))
df_scores = clf.negative_outlier_factor_

esik_deger = np.sort(df_scores)[13] 
baski_deger = df[df_scores == esik_deger] 
ar_extreme = df_scores > esik_deger
df_extreme = df[~ar_extreme]
# print(df_extreme)
# print(baski_deger)
np_extremenoindex = df_extreme.to_records(index = False)
print(np_extremenoindex)
np_extremenoindex[:] = baski_deger.to_records(index=False)
print(np_extremenoindex)
print(df[~ar_extreme])
df[~ar_extreme] = pd.DataFrame(np_extremenoindex, index=df[~ar_extreme].index)
 
print(df[:52862])

 
 