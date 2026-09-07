import seaborn as sea
import pandas as pd
planets = sea.load_dataset("planets")
print(planets.head())
print(planets.info())
print(planets.dtypes)
planets.method = pd.Categorical(planets.method)
print(planets.info())
#veri seti oluşumu nasıl oluştu?