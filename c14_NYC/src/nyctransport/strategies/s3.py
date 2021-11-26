import io

import pandas as pd
from airflow.hooks.base import BaseHook
from minio import Minio
from pandas.errors import EmptyDataError, ParserError


def write_minio_object(
        df,
        pandas_write_callable,
        bucket,
        path,
        pandas_write_callable_kwargs=None
):
    s3_conn = BaseHook.get_connection(conn_id="s3")
    minio_client = Minio(
        s3_conn.extra_dejson["host"].split("://")[1],
        access_key=s3_conn.extra_dejson["aws_access_key_id"],
        secret_key=s3_conn.extra_dejson["aws_secret_access_key"],
        secure=False,
    )
    bytes_buffer = io.BytesIO()
    pandas_write_method = getattr(df, pandas_write_callable.__name__)
    pandas_write_method(bytes_buffer, **pandas_write_callable_kwargs)
    nbytes = bytes_buffer.tell()
    bytes_buffer.seek(0)
    minio_client.put_object(
        bucket_name=bucket,
        object_name=path,
        length=nbytes,
        data=bytes_buffer
    )


def get_minio_object(
        pandas_read_callable,
        bucket,
        paths,
        pandas_read_callable_kwargs=None
):
    s3_conn = BaseHook.get_connection(conn_id="s3")
    minio_client = Minio(
        s3_conn.extra_dejson["host"].split("://")[1],
        access_key=s3_conn.extra_dejson["aws_access_key_id"],
        secret_key=s3_conn.extra_dejson["aws_secret_access_key"],
        secure=False,
    )

    if isinstance(paths, str):
        if paths.startswith("[") and paths.endswith("]"):
            paths = eval(paths)
        else:
            paths = [paths]

    if pandas_read_callable_kwargs is None:
        pandas_read_callable_kwargs = {}

    dfs = []
    for path in paths:
        minio_object = minio_client.get_object(bucket_name=bucket, object_name=path)
        try:
            df = pandas_read_callable(minio_object, **pandas_read_callable_kwargs)
        except (EmptyDataError, ParserError):
            df = pd.DataFrame()
        dfs.append(df)
    try:
        result = pd.concat(dfs)
    except ValueError:
        result = pd.DataFrame()

    return result
