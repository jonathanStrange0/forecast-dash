import sqlite3
import pandas as pd

def collect_bike_data(db_path):
    """
    Reads in a database of bike sales
    :param db_path: the path to the database
    :return: a pandas dataframe with bike sales information
    """
    con = sqlite3.connect(db_path)

    sql = 'SELECT * FROM orderlines LEFT OUTER JOIN bikes ' \
          'ON "product.id" =  "bike.id" ' \
          'LEFT OUTER JOIN bikeshops ' \
          'ON "customer.id" = "bikeshop.id"'

    df = pd.read_sql(sql, con)
    con.close()

    df['price_ext'] = df.price * df.quantity
    df.index = pd.to_datetime(df['order.date'])

    return df