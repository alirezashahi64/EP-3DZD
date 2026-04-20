import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score

data = np.load("features/ep3dzd_features.npz", allow_pickle=True)
feat_dict = data["features_dict"].item()

X = np.array(list(feat_dict.values()))
y = np.random.rand(len(X))  # replace with real pK

model = RandomForestRegressor(n_estimators=100)

y_pred = cross_val_predict(model, X, y, cv=5)

print("R2:", r2_score(y, y_pred))
