import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from c03_scheduling._calculate_stats import _calculate_stats

dag = DAG(
    dag_id="06_templated_query",
    schedule_interval="@daily",
    start_date=dt.datetime(year=2019, month=1, day=1),
    end_date=dt.datetime(year=2019, month=1, day=5),
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data/events && "
        "curl -o /data/events.json "
        "http://events_api:5000/events?"
        "start_date={{execution_date.strftime('%Y-%m-%d')}}&"
        "end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
    ),
    dag=dag,
)

calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": "/data/events.json", "output_path": "/data/stats.csv"},
    dag=dag,
)

fetch_events >> calculate_stats
