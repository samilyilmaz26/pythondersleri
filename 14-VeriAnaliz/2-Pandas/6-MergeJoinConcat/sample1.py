# Concat

import numpy as np
import pandas as pd

ds1 = {
    "İst": ["100","200","300","400"],
    "Ank":["-1","-2","-3","-4"],
    "İzmir":["1000","2000","3000","4000"],
}
ds2 = {
    "İst": ["500","600","700","800"],
    "Ank":["-5","-6","-7","-8"],
    "İzmir":["5000","6000","7000","8000"],
}
df1 = pd.DataFrame(ds1,index = ["Ocak","Şubat","Mart","Nisan"])
df2 = pd.DataFrame(ds2,index = ["Mayıs","Haziran","Temmuz","Ağustos"] )
print(df1)
print(df2)
print(pd.concat([df1,df2]))
print(pd.concat([df1,df2] ,axis=1))