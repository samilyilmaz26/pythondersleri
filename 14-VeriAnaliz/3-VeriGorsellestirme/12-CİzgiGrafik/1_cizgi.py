import  seaborn as sea
fm  = sea.load_dataset("fmri")
 
print(fm.head())
print(fm.groupby("timepoint")["signal"].describe())
print(sea.lineplot(x="timepoint", y="signal", data=fm))
print(sea.lineplot(x="timepoint", y="signal",hue= "event" , data=fm))
print(sea.lineplot(x="timepoint", y="signal",
                   hue= "event" ,style = "event", data=fm))
# print(sea.lineplot(x="timepoint", y="signal",
#                    hue= "region" , data=fm))
# print(sea.lineplot(x="timepoint", y="signal",
#                    hue= "event" ,style = "event",
#                    markers=True , dashes=False,
#                    data=fm))
