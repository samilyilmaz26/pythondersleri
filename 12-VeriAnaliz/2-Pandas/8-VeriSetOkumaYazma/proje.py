import  pandas as   pd
df = pd.read_csv("country_vaccinations.csv")
 
print(df)
#df2 = df.drop(labels="id",axis=1)
#print(df2)
#df2.to_csv("new_tweets.csv",index=False)
# dfFatura = pd.read_excel("fatura.xlsx")
# print(dfFatura)
# dfKorona = pd.read_html("https://www.worldometers.info/coronavirus/",header=0)
# print(dfKorona)