import xgboost as xgb
import pandas as pd
import numpy as np
from datetime import datetime
from functions.ts_feature_extractor import extract_features_from_dataframe

def predict_n_future_sales(data, n_future, period):
    '''

    :param data:
    :param n_future:
    :param period:
    :return:
    '''
    df, y = make_future_dataframe(data, n_future, period)

    X = df.iloc[:-n_future, :].values
    y = y.iloc[:-n_future].values

    regressor = xgb.XGBRegressor(max_depth=6,
                                 learning_rate=0.6,
                                 n_estimators=500,
                                 gamma=0.01
                    )

    regressor.fit(X,y)

    future_data = regressor.predict(df.iloc[-n_future:,:].values)

    return future_data

def make_future_dataframe(df, n_future, period):
    index = df.index
    # print(index)
    future_index = pd.date_range(index[-1], periods=n_future, freq=period)
    # print(future_index)
    future_df = pd.DataFrame([np.nan]*n_future, index=future_index)

    whole_df = pd.concat([df, future_df])
    # print(future_df)
    return extract_features_from_dataframe(whole_df, 'price_ext', lag=3)