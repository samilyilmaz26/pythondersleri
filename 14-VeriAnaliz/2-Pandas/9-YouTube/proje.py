import pandas as pd     
yt = pd.read_csv("USvideos.csv")
print(yt)
print(yt.head(5))
print(len(yt.index))
print(yt.columns)
print(yt["likes"])
print(yt["likes"].mean())
print(yt["views"].max())
maxViews = yt["views"].max()
print (maxViews)
maxvideo =  yt[yt["views"] == maxViews]
print(yt.groupby("category_id").mean())
print(yt.groupby("category_id").mean()["likes"])
print(yt.groupby("category_id").mean()[["likes"]])
print(yt["category_id"].value_counts()) 


