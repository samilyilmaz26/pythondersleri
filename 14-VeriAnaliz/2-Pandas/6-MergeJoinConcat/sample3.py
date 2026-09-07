#Merge  Sutun  bazında olur
import numpy as np
import pandas as pd
ds1 = {
    "Ankara" : ["100","200","300"],
    "İstanbul" : ["10","20","30"],
    "anahtar" : ["1","2","3"]
}
df1 = pd.DataFrame(ds1,index = ["Ocak","Şubat","Mart"]) 
print(df1)

ds2 = {
    "Ankara" : ["50000","60000","70000","80000"],
    "İstanbul" : ["50","60","70","80"],
    "anahtar" : ["1","2","3","4"]
}
df2 = pd.DataFrame(ds2,index = ["Ocak","Şubat","Mart","Nisan"]) 
print(df2)
print(pd.merge(df1,df2,how ="inner",on = "anahtar"))
print(pd.merge(df1,df2,how ="outer",on = "anahtar"))
