import requests
from airflow.hooks.base import BaseHook
from airflow.hooks import S3_hook


def _download_taxi_data():
    taxi_conn = BaseHook.get_connection(conn_id="taxi")
    s3_hook = S3_hook.S3Hook(aws_conn_id="s3")

    url = f"http://{taxi_conn.host}"
    response = requests.get(url)
    files = response.json()

    exported_files = []
    for filename in [f["name"] for f in files]:
        response = requests.get(f"{url}/{filename}")
        s3_key = f"raw/taxi/{filename}"
        try:
            s3_hook.load_string(
                string_data=response.text,
                key=s3_key,
                bucket_name="datalake"
            )
            print(f"Uploaded {s3_key} to MinIO.")
            exported_files.append(s3_key)
        except ValueError:
            print(f"File {s3_key} already exists.")

    return exported_files
