import pandas as pd

def aggregate_time_series(df, time_unit):
    """

    :param df: Dataframe containing the time series data that needs to be aggregated.
    :param time_unit: one of "day", "week", "month", "quarter", "year".
    :return: a dataframe that has a time series aggregated by the chosen time unit
    """
    # time aggregation unit dictionary`
    taud = {
        "Day":"D",
        "Week" : "W",
        "Month" : "M",
        "Quarter" : "Q",
        "Year" : "Y"
    }

    return df[["price_ext"]].resample(taud[time_unit]).sum(), taud[time_unit]