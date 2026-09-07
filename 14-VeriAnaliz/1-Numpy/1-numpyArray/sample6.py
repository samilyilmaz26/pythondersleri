import numpy as np

detArray =  np.random.randint(1,100,25)
print(detArray)
detArray = detArray.reshape(5,5)
print(detArray)
print(np.linalg.det(detArray))
print(round(np.linalg.det(detArray)))
detArray2 = np.array([[1,2],[3,4]])
print(detArray2)
print(round(np.linalg.det(detArray2)))