import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from c02_anatomy.curl_thespacedevs import curl_command_str
from c02_anatomy.get_pictures import _get_pictures

dag = DAG(
    dag_id="d0206_invoking_python_operator",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)

download_launches = BashOperator(
    task_id="download_launches",
    bash_command=curl_command_str,
    dag=dag,
)

get_pictures = PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,
    dag=dag
)

download_launches >> get_pictures
