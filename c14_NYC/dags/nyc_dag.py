import io

import airflow.utils.dates
import pandas as pd
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from nyctransport.operators.pandas_operator import PandasOperator
from nyctransport.operators.s3_to_postgres import MinioPandasToPostgres
from nyctransport.strategies.citi_bike import citi_bike_api_to_s3
from nyctransport.strategies.s3 import write_minio_object, get_minio_object
from nyctransport.strategies.taxi import _download_taxi_data
from nyctransport.transformations.taxi import transform_taxi_data
from nyctransport.transformations.citi_bike import transform_citi_bike_data

dag = DAG(
    dag_id="nyc_dag",
    schedule_interval="*/15 * * * *",
    start_date=airflow.utils.dates.days_ago(1),
    catchup=False,
)

download_citi_bike_data = PythonOperator(
    task_id="download_citi_bike_data",
    python_callable=citi_bike_api_to_s3,
    dag=dag
)

download_taxi_data = PythonOperator(
    task_id="download_taxi_data",
    python_callable=_download_taxi_data,
    dag=dag
)

process_citi_bike_data = PandasOperator(
    task_id="process_citi_bike_data",
    input_callable=get_minio_object,
    input_callable_kwargs={
        "pandas_read_callable": pd.read_json,
        "bucket": "datalake",
        "paths": "raw/citibike/{{ ts_nodash }}.json",
    },
    transform_callable=transform_citi_bike_data,
    output_callable=write_minio_object,
    output_callable_kwargs={
        "bucket": "datalake",
        "path": "processed/citibike/{{ ts_nodash }}.parquet",
        "pandas_write_callable": pd.DataFrame.to_parquet,
        "pandas_write_callable_kwargs": {"engine": "auto"},
    },
    dag=dag,
)

process_taxi_data = PandasOperator(
    task_id="process_taxi_data",
    input_callable=get_minio_object,
    input_callable_kwargs={
        "pandas_read_callable": pd.read_csv,
        "bucket": "datalake",
        "paths": "{{ ti.xcom_pull(task_ids='download_taxi_data') }}",
    },
    transform_callable=transform_taxi_data,
    output_callable=write_minio_object,
    output_callable_kwargs={
        "bucket": "datalake",
        "path": "processed/taxi/{{ ts_nodash }}.parquet",
        "pandas_write_callable": pd.DataFrame.to_parquet,
        "pandas_write_callable_kwargs": {"engine": "auto"},
    },
    dag=dag,
)

taxi_to_db = MinioPandasToPostgres(
    task_id="taxi_to_db",
    dag=dag,
    minio_conn_id="s3",
    minio_bucket="datalake",
    minio_key="processed/taxi/{{ ts_nodash }}.parquet",
    pandas_read_callable=pd.read_parquet,
    postgres_conn_id="result_db",
    postgres_table="taxi_rides",
    pre_read_transform=lambda x: io.BytesIO(x.data),
)

citi_bike_to_db = MinioPandasToPostgres(
    task_id="citi_bike_to_db",
    dag=dag,
    minio_conn_id="s3",
    minio_bucket="datalake",
    minio_key="processed/citibike/{{ ts_nodash }}.parquet",
    pandas_read_callable=pd.read_parquet,
    postgres_conn_id="result_db",
    postgres_table="citi_bike_rides",
    pre_read_transform=lambda x: io.BytesIO(x.data),
)

download_citi_bike_data >> process_citi_bike_data >> citi_bike_to_db
download_taxi_data >> process_taxi_data >> taxi_to_db
