import pandas as pd
import numpy as np
from datetime import datetime


def extract_features_from_dataframe(df, value_column, lag):
    """
    Function to take a datetime indexed dataframe and feature engineer that dataframe to become something
    that can be used in a supervised ML problem.

    Currently only supports single variate prediction.

    :param df: dataframe containing all features and time series value we wish to predict.
        dataframe shuold be indexed by a datetime index and all columns will be assumed
        to be features taken as part of the time series except value_column.
    :param value_column: the value we wish to predict after turing this time series problem into a supervised ml problem
    :return: Dataframe with features and lag values added
    """

    # check to make sure we have a datetime index
    if type(pd.DatetimeIndex([datetime.now()])) != type(df.index):
        df.index = pd.to_datetime(df.index)

    # Create return dataframe
    feature_df = pd.DataFrame({'value': df[value_column].values}, index=df.index)

    # Extract time based features
    feature_df['year'] = [df.index[i].year for i in range(len(df.index))]
    feature_df['quarter'] = [df.index[i].quarter for i in range(len(df.index))]
    feature_df['month'] = [df.index[i].month for i in range(len(df.index))]
    feature_df['week'] = [df.index[i].week for i in range(len(df.index))]
    feature_df['day'] = [df.index[i].day for i in range(len(df.index))]
    feature_df['weekday'] = [df.index[i].weekday() for i in range(len(df.index))]

    # Drop any features just created that are constants:
    feature_df = feature_df.loc[:, feature_df.apply(pd.Series.nunique) != 1]

    # Generate Lag features
    lagged_values = [df.shift(i) for i in range(lag + 1)]
    lag_df = pd.concat(lagged_values[1:])
    lag_cols = ['value (t-' + str(x) + ')' for x in range(1, lag + 1)]
    lag_df.columns = lag_cols

    # Generate rolling window stats


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