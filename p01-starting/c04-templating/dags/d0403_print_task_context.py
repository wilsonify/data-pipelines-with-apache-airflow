import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="listing_4_03",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)


def _print_context(**kwargs):
    """
    example context
    {
     'dag': <DAG: print_context>,
     'ds': '2019-07-04',
     'next_ds': '2019-07-04',
     'next_ds_nodash': '20190704',
     'prev_ds': '2019-07-03',
     'prev_ds_nodash': '20190703',
     ...
    }
    """
    print(kwargs)


print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context, dag=dag
)
