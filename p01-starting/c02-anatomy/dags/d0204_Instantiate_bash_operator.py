import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

from c02_anatomy.curl_thespacedevs import curl_command_str

dag = DAG(
    dag_id="d0204_Instantiate_bash_operator",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)

download_launches = BashOperator(
    task_id="download_launches",
    bash_command=curl_command_str,
    dag=dag,
)
