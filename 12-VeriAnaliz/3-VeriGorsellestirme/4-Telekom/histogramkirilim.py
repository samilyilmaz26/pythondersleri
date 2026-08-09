
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("telecom_users.csv")
 

sns.catplot(x= "StreamingTV", y="MonthlyCharges", hue="Partner" , kind="point",data=df)

plt.show()
