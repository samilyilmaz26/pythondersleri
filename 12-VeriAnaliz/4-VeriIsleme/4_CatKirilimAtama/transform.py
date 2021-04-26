import numpy as np 
import pandas as pd

s = pd.Series(range(3))
print(s)  
s =  s.transform([np.sqrt, np.exp])
print(s)

df = pd.DataFrame({
    "Date": [
        "2015-05-08", "2015-05-07", "2015-05-06", "2015-05-05",
        "2015-05-08", "2015-05-07", "2015-05-06", "2015-05-05"],
    "Data": [5, 8, 6, 1, 50, 100, 60, 120],
})
print(df) 
print(df.groupby("Date")["Data"].mean())
print (df.groupby('Date')['Data'].transform('sum'))
 
 
 