import seaborn as sea
import pandas as pd
pl = sea.load_dataset("planets")
print(pl.isnull().values.any()) # eksik değer varmı
print(pl.isnull().sum()) 
pl["orbital_period"].fillna(0, inplace = True) 
print(pl.isnull().sum()) 
pl["distance"].fillna(pl.distance.mean(), inplace = True) 
print(pl.isnull().sum()) 