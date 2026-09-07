import sys
print(".............")
print(sys.executable) 
print(".............")
import numpy as np
import pandas as pd

lb_list = ["Şamil","Selen","Peri","Özlem","Zeynep"]
data_list = [10,20,30,40,50]
data_series = pd.Series(data = data_list)
print(data_series)
data_series2 = pd.Series(data = data_list,index = lb_list)
print(data_series2)

array = np.array([10,20,30,40,50])
data_series = pd.Series(data = array)
print(data_series)
data_series2 = pd.Series(data=array ,index=lb_list)
print(data_series2)