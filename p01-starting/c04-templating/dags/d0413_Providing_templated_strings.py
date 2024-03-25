import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

from c04_templating import _get_data2

dag = DAG(
    dag_id="listing_4_13",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
)

get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data2,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wikipageviews.gz",
    },
    dag=dag,
)
