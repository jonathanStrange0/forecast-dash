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
    # :param lag_offset: For rolling window calculations, change the lookback parameter by some amount
    :return: Dataframe with features and lag values added
    """

    # check to make sure we have a datetime index
    if type(pd.DatetimeIndex([datetime.now()])) != type(df.index):
        df.index = pd.to_datetime(df.index)

    # Create return dataframe
    feature_df = pd.DataFrame(index=df.index)

    # Extract time based features
    feature_df['year'] = [df.index[i].year for i in range(len(df.index))]
    feature_df['quarter'] = [df.index[i].quarter for i in range(len(df.index))]
    feature_df['month'] = [df.index[i].month for i in range(len(df.index))]
    feature_df['week'] = [df.index[i].week for i in range(len(df.index))]
    feature_df['day'] = [df.index[i].day for i in range(len(df.index))]
    feature_df['weekday'] = [df.index[i].weekday() for i in range(len(df.index))]

    # Drop any features just created that are constants:
    feature_df = feature_df.loc[:, feature_df.apply(pd.Series.nunique) != 1]

    # # Generate Lag features
    # lagged_values = [df.shift(i) for i in range(lag + 1)]
    # lag_df = pd.concat(lagged_values[1:], axis=1)
    # print(lag_df.head())
    # lag_cols = ['value (t-' + str(x) + ')' for x in range(1, lag + 1)]
    # print(lag_cols)
    # lag_df.columns = lag_cols
    #
    # # Generate rolling window stats
    # window = lag_df[['value (t-' + str(lag) + ')']].rolling(window=(lag))
    # lag_df['rolling_mean'] = window.mean()
    # lag_df['rolling_min'] = window.min()
    # lag_df['rolling_max'] = window.max()

    # Build the feature dataframe
    # feature_df = pd.concat([feature_df, lag_df], axis=1)
    feature_df.dropna(inplace=True)

    return feature_df, df[value_column]
