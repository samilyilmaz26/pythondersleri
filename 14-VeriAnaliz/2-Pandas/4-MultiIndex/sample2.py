import numpy as np
import pandas as pd
from numpy.random import randn

outerIndex = ["ç1","ç1","ç1","ç2","ç2","ç2","ç3","ç3","ç3"  ]
innerIndex = ["ocak","şubat","mart", "ocak","şubat","mart" ,"ocak","şubat","mart"  ]
list = list(zip(outerIndex,innerIndex))
print(list)
h = pd.MultiIndex.from_tuples(list)
print(h)

df = pd.DataFrame(randn(9,3)*10,h,columns = ["Ankara","İstanbul" ,"İzmir"])
df.index.names = ["Çeyrekler","Aylar"]
#xs
print(df)
print(df.xs("ç2"))
print(df.xs("ç3").xs("mart"))
print(df.xs("ç3").xs("mart").xs("İzmir"))
print(df.xs("mart",level = "Aylar")) 
 