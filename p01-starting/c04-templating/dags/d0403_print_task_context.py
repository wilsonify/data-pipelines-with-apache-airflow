import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

from c04_templating import print_context

dag = DAG(
    dag_id="listing_4_03",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)

print_context = PythonOperator(
    task_id="print_context",
    python_callable=print_context,
    dag=dag
)
