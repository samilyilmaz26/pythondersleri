#Join Satır bazında olur
import numpy as np
import pandas as pd
ds1 = {
    "İst" : ["100","200","300","400"],
    "Ank" : ["1000","2000","3000","4000"],
}
ds2 = {
    "İzmir" : ["100","200","300"],
    "Adana" : ["1000","2000","3000"],
}
df1 = pd.DataFrame(ds1,index = ["Ocak","Şubat","Mart","Nisan"]) 
df2 = pd.DataFrame(ds2,index = ["Ocak","Şubat","Mart"])
print(df1)
print(df2)
print(df1.join(df2))
print(df2.join(df1))