import numpy as np
import pandas as pd


def transform_taxi_data(df):
    if df is None:
        return df
    if df.shape[0] < 1:
        df = pd.DataFrame(columns=[
            "starttime",
            "start_location_id",
            "stoptime",
            "end_location_id"
        ])
        return df
    try:
        pickup = df["pickup_datetime"]
    except KeyError:
        df["pickup_datetime"] = np.nan
        pickup = df["pickup_datetime"]

    try:
        dropoff = df["dropoff_datetime"]
    except KeyError:
        df["dropoff_datetime"] = np.nan
        dropoff = df["dropoff_datetime"]

    pickup_datetime = pd.to_datetime(pickup)
    dropoff_datetime = pd.to_datetime(dropoff)
    df["pickup_datetime"] = pickup_datetime
    df["dropoff_datetime"] = dropoff_datetime

    dropoff_minus_pickup = df["dropoff_datetime"] - df["pickup_datetime"]
    dropoff_minus_pickup_s = dropoff_minus_pickup.dt.total_seconds()
    dropoff_minus_pickup_int = dropoff_minus_pickup_s.astype(int)
    df["tripduration"] = dropoff_minus_pickup_int
    df = df.rename(columns={
        "pickup_datetime": "starttime",
        "pickup_locationid": "start_location_id",
        "dropoff_datetime": "stoptime",
        "dropoff_locationid": "end_location_id",
    })
    df = df.drop(["trip_distance"], axis=1, errors='ignore')
    return df
