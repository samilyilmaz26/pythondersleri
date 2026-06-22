import numpy  as np
















A = np.array([
    [0, 3, 2],
    [1, 0, 2],
    [0, 2, 0]
], dtype=float)
print(A)

row_sums = A.sum(axis=1)
col_sums = A.sum(axis=0)
# s is coofficient to calculate X matrix (normalized matrix)

s = 1 / max(row_sums.max(), col_sums.max())
print(s)
# // Normalizasyon işlemi
X = s * A 
print(X)
# I is identity matrix  
I = np.eye(A.shape[0])
print(I)
# T Matrix is calculated Total  
# 
T = X @ np.linalg.inv(I - X)   
#   T times           I-X inverse    
# 4. D ve R değerleri
D = T.sum(axis=1)  #  row Totals 
R = T.sum(axis=0)  #  column Totals

criteria = ["Price", "Quality", "Delivery"]
print("results based on Critera for D-R:")
for i in range(len(criteria)):
    print(f"{criteria[i]} -> D: {D[i]:.3f}, R: {R[i]:.3f}, D-R: {D[i]-R[i]:.3f}")
print("results based on Critera for D+R:")
for i in range(len(criteria)):
    print(f"{criteria[i]} -> D: {D[i]:.3f}, R: {R[i]:.3f}, D+R: {D[i]+R[i]:.3f}")
 