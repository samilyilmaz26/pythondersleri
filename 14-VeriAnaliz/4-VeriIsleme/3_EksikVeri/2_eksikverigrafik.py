#%%
import  missingno as msno
import seaborn as sns
df =sns.load_dataset('planets')
print (df.isnull().sum())
print(msno.matrix(df))
print(msno.heatmap(df))

# %%
