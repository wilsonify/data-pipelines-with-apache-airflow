import geopandas
import numpy as np
import pandas as pd


def transform_citi_bike_data(df):
    if df is None:
        return df
    if df.shape[0] < 1:
        df = pd.DataFrame(columns=[
            "tripduration",
            "starttime",
            "start_location_id",
            "stoptime",
            "end_location_id"
        ])
        return df

    try:
        start_station_longitude = df["start_station_longitude"]
    except KeyError:
        df["start_station_longitude"] = np.nan
        start_station_longitude = df["start_station_longitude"]
    try:
        start_station_latitude = df["start_station_latitude"]
    except KeyError:
        df["start_station_latitude"] = np.nan
        start_station_latitude = df["start_station_latitude"]

    try:
        end_station_longitude = df["end_station_longitude"]
    except KeyError:
        df["end_station_longitude"] = np.nan
        end_station_longitude = df["end_station_longitude"]

    try:
        end_station_latitude = df["end_station_latitude"]
    except KeyError:
        df["end_station_latitude"] = np.nan
        end_station_latitude = df["end_station_latitude"]

    # Map citi bike lat,lon coordinates to taxi zone ids
    taxi_zones = geopandas.read_file(
        "https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip"
    ).to_crs("EPSG:4326")
    start_gdf = geopandas.GeoDataFrame(
        df,
        crs="EPSG:4326",
        geometry=geopandas.points_from_xy(
            start_station_longitude,
            start_station_latitude
        ))
    end_gdf = geopandas.GeoDataFrame(
        df,
        crs="EPSG:4326",
        geometry=geopandas.points_from_xy(
            end_station_longitude,
            end_station_latitude
        ))
    df_with_zones = geopandas.sjoin(
        start_gdf,
        taxi_zones,
        how="left",
        op="within"
    )
    df_with_zones = df_with_zones.rename(columns={"LocationID": "start_location_id"})
    end_zones = geopandas.sjoin(end_gdf, taxi_zones, how="left", op="within")
    end_zones = end_zones.rename(columns={"LocationID": "end_location_id"})
    df_with_zones["end_location_id"] = end_zones["end_location_id"]
    return df_with_zones[[
        "tripduration",
        "starttime",
        "start_location_id",
        "stoptime",
        "end_location_id",
    ]]
