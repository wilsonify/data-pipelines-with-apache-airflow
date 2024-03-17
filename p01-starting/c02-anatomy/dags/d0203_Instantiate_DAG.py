import airflow
from airflow import DAG

dag = DAG(
    dag_id="d0203_Instantiate_DAG",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)
