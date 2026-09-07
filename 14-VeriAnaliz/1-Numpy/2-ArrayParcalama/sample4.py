import numpy as np
arr= np.arange(1,21)
print(arr)
arr  = arr.reshape(4,5)
print(arr)
print(arr[0,1])
print(arr[:,:2])
print(arr[:2,:2])
print(arr[2:])