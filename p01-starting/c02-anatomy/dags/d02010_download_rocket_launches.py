from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from c02_anatomy.curl_thespacedevs import curl_command_str
from c02_anatomy.echo_line_count import notify_cmd_str
from c02_anatomy.get_pictures import _get_pictures

dag = DAG(
    dag_id="d02010_download_rocket_launches",
    description="Download rocket pictures of recently launched rockets.",
    start_date=days_ago(14),
    schedule_interval="@daily",
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

notify = BashOperator(
    task_id="notify",
    bash_command=notify_cmd_str,
    dag=dag,
)

# Defining the order of task execution
download_launches >> get_pictures >> notify
