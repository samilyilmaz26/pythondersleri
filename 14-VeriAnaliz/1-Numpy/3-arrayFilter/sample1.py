import numpy as np
arr = np.arange(1,10)
print(arr > 3)
newArray = arr > 3
print(newArray)
print(arr[newArray])