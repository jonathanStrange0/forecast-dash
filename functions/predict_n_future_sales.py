import xgboost as xgb
import pandas as pd
from datetime import datetime

def predict_n_future_sales(data, n_future):

    X = data[:,:-1]
    y = data[:,-1:]

    regressor = xgb.XGBRegressor(max_depth=6,
                                 learning_rate=0.6,
                                 n_estimators=500,
                                 gamma=0.01
                    )

    regressor.fit(X,y)

    future_data = regressor.predict(X)

    return future_data