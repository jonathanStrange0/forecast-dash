import xgboost as xgb
import pandas as pd
from datetime import datetime

def predict_n_future_sales(data, n_future):

    # ### APPLY FEATURE EXTRACTION BEFORE PASSING data TO THIS FUNCTION ###
    # prediction_lag = 6
    # prediction_lead = n_future
    # df = pd.DataFrame(data.values[:,:])
    # columns = [df.shift(-i) for i in range(0, prediction_lag + 1)]
    # df_X = pd.concat(columns,axis=1)
    # df_all = pd.concat([df_X, df.shift(-(prediction_lead + prediction_lag))], axis=1)
    # df_all = df_all.iloc[:-(prediction_lead + prediction_lag), :]
    # df_all.fillna(0, inplace=True)
    # dataset = df_all.values



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