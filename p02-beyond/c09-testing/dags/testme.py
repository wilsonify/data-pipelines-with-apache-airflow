import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(dag_id="testme", start_date=airflow.utils.dates.days_ago(3), schedule_interval=None) as dag:
    t1 = DummyOperator(task_id="test", dag=dag)
    for tasknr in range(5):
        t2 = BashOperator(
            task_id=f"test{tasknr}",
            bash_command=f"echo '{tasknr}'",
            dag=dag
        )
        t2 >> t1
