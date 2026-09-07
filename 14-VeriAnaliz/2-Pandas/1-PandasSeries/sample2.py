import numpy as np
import pandas as pd

lb_list = ["Şamil","Selen","Peri","Özlem","Zeynep"]
array = np.array([10,20,30,40,50])
data_series = pd.Series(data = array)
print(data_series)
data_series2 = pd.Series(data=array ,index=lb_list)
print(data_series2)