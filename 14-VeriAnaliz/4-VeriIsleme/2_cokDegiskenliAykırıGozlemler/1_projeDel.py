 
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor 

df = sns.load_dataset("diamonds")
 
df = df.select_dtypes(include= ["float64","int64"])
df = df.dropna()
clf = LocalOutlierFactor(n_neighbors=20 ,contamination=0.1)
# contamination‘auto’ or float, default=’auto’
# The amount of contamination of the data set, i.e. the proportion of outliers in the data set. When fitting this is used to define the threshold on the scores of the samples.

# if ‘auto’, the threshold is determined as in the original paper,

# if a float, the contamination should be in the range [0, 0.5]
# bulaşma 
print(clf.fit_predict(df))
df_scores = clf.negative_outlier_factor_
print(df_scores[0:10])
print(np.sort(df_scores)[0:20] )
esik_deger = np.sort(df_scores)[13] 
print(esik_deger)
ar_extreme = df_scores>esik_deger
print(ar_extreme)
new_df = df[df_scores > esik_deger]
print(new_df)