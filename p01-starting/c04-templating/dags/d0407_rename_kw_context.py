import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

from c04_templating.print_context import _print_context2

dag = DAG(
    dag_id="listing_4_07",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)

print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context2, dag=dag
)
