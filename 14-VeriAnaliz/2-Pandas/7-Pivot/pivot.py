import numpy as np
import pandas as pd
from numpy.random import randn
 
df = pd.DataFrame ({
    "Yıl":["2000","2001","2002","2000","2001","2002", "2000","2001","2002"],
    "Satış": [100000,200000,250000,1500,9000,6000,1100,7700 ,8200],
    "Ürün": ["Çorap","Çorap","Çorap" ,"Pantolon","Pantolon","Pantolon","Etek","Etek","Etek"]

})
print(df)
print(df.pivot_table(index="Yıl", columns="Ürün",values="Satış"))
print(df.pivot_table(index="Ürün", columns="Yıl",values="Satış"))

 