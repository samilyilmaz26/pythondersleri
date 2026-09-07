import seaborn as sea
import pandas as pd
planets = sea.load_dataset("planets")

print(planets.shape)
print(planets.columns)
print(planets.describe())
print(planets.describe().T) #yanlızca sayısal değişkenler eksik değerler alınmaz
print(planets.describe(include="all").T) # kategorik değişkenlede alınır