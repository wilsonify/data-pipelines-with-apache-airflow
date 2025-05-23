from datetime import datetime
from os.path import dirname

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from c04_templating import _get_data, _get_data2
from c04_templating import print_context
from c04_templating.fetch_pageviews import _fetch_pageviews
from dags import (
    d0401_download_wikipedia_pageviews_bash,
    d0403_print_task_context,
    d0405_download_wikipedia_pageviews_python,
    d0407_rename_kw_context,
    d0408_printing_start_end_interval,
    d0413_Providing_templated_strings,
    d0415_Read_pageviews_for_page_names,
    d0418_INSERT_to_Postgres_python,
    d0420_INSERT_to_Postgres_postgres,
)

path_to_data = f"{dirname(__file__)}/data"


def validate_dag(module):
    module_vars = vars(module)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_d0401_download_wikipedia_pageviews_bash():
    validate_dag(d0401_download_wikipedia_pageviews_bash)


def test_d0403_print_task_context():
    validate_dag(d0403_print_task_context)


def test_d0405_download_wikipedia_pageviews_python():
    validate_dag(d0405_download_wikipedia_pageviews_python)


def test_d0407_rename_kw_context():
    validate_dag(d0407_rename_kw_context)


def test_d0408_printing_start_end_interval():
    validate_dag(d0408_printing_start_end_interval)


def test_d0413_Providing_templated_strings():
    validate_dag(d0413_Providing_templated_strings)


def test_d0415_Read_pageviews_for_page_names():
    validate_dag(d0415_Read_pageviews_for_page_names)


def test_d0418_INSERT_to_Postgres_python():
    validate_dag(d0418_INSERT_to_Postgres_python)


def test_d0420_INSERT_to_Postgres_postgres():
    validate_dag(d0420_INSERT_to_Postgres_postgres)


def test_bash_operator_execution():
    bash_task = BashOperator(
        task_id="test_bash_task",
        bash_command="echo 'Hello, world!'"
    )
    bash_task.execute({})


def test_get_data_bash():
    # Format the command string outside of bash_command
    dest_dir = "data/output"
    filename = "pageviews-20190202-120000.gz"
    command_list = [
        "pwd", "&&",
        "mkdir", "-p", f"{dest_dir}", "&&",
        "rm", "-f", f"{dest_dir}/{filename}", "&&",
        "curl", f"https://dumps.wikimedia.org/other/pageviews/2019/2019-02/{filename}",
        "-o", f"{dest_dir}/{filename}"
    ]
    command_str = " ".join(command_list)
    BashOperator(task_id="get_data", bash_command=command_str).execute({})


def test_print_context():
    PythonOperator(
        task_id="print_context",
        python_callable=print_context,
    ).execute({})


def test_get_data_python():
    PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
    ).execute({})


def test_get_data2():
    PythonOperator(
        task_id="get_data",
        python_callable=_get_data2,
        op_kwargs={
            "year": "{{ execution_date.year }}",
            "month": "{{ execution_date.month }}",
            "day": "{{ execution_date.day }}",
            "hour": "{{ execution_date.hour }}",
            "output_path": "/tmp/wikipageviews.gz",
        },

    ).execute({})


def test_fetch_pageviews():
    PythonOperator(
        task_id="fetch_pageviews",
        python_callable=_fetch_pageviews,
        op_kwargs={
            "pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"},
            "source_dir": "data/output/pageviews",
            "dest_dir": "data/output/pageviewcounts"
        },
    ).execute({})


def test_pg():
    PostgresOperator(
        task_id="write_to_postgres",
        postgres_conn_id="my_postgres",
        sql="postgres_query.sql",
    ).execute({})
