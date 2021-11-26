import json

import requests
from airflow.hooks.base import BaseHook
from requests.auth import HTTPBasicAuth
from airflow.hooks import S3_hook


def citi_bike_api_to_s3(ts_nodash, **_):
    citibike_conn = BaseHook.get_connection(conn_id="citibike")

    response = requests.get(
        url=f"http://{citibike_conn.host}:{citibike_conn.port}/recent/minute/15",
        auth=HTTPBasicAuth(citibike_conn.login, citibike_conn.password)
    )
    data = response.json()

    s3_hook = S3_hook.S3Hook(aws_conn_id="s3")
    s3_hook.load_string(
        string_data=json.dumps(data),
        key=f"raw/citibike/{ts_nodash}.json",
        bucket_name="datalake",
    )
