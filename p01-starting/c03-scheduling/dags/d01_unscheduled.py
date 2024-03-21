from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from c03_scheduling._calculate_stats import _calculate_stats

dag = DAG(
    dag_id="01_unscheduled",
    start_date=datetime(2019, 1, 1),
    schedule_interval=None
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data/events && "
        "curl -o /data/events.json http://events_api:5000/events"
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
