import numpy as np
arr = np.arange(25)
print(arr)
print(arr.reshape(5,5)) # 5 x 5 =  25 tek boyutlu matrisi 2 boyuta çevirir.)
newArray = np.random.randint(1,100,10)
print (newArray)
print(newArray.max())
print(newArray.min())
print(newArray.sum())
print(newArray.mean())
print(newArray.argmin()) # En küçük eleman n.indekste
print(newArray.argmax() )# En büyük eleman n.indekste