#%%
import  pandas_datareader as pr
import  pandas as pd

df = pr.get_data_yahoo("AAPL", start= "2017-01-01", end = "2019-12-31")
print(df.head())
print(df.shape)
dfKapanis =  df["Close"]

print(dfKapanis.plot())
print(dfKapanis.index)
dfKapanis.index = pd.DatetimeIndex(dfKapanis.index)
print(dfKapanis.index)

#pip install pandas_datareader
# %%
