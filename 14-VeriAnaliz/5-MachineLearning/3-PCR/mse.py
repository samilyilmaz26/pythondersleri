from sklearn.metrics import mean_squared_error
y_true = [3000, -500, 2000, 7000]
y_pred = [2500, 0, 2000, 8000]
print(mean_squared_error(y_true, y_pred ,squared=False))