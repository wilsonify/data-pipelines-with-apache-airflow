from os.path import dirname

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from c03_scheduling._calculate_stats import _calculate_stats, _calculate_stats2
from dags import (
    d01_unscheduled,
    d02_daily_schedule,
    d03_with_end_date,
    d04_time_delta,
    d05_query_with_dates,
    d06_templated_query,
    d07_templated_query_ds,
    d08_templated_path,
    d09_no_catchup,
    d10_non_atomic_send,
    d11_atomic_send,

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


def test_d01_unscheduled():
    validate_dag(d01_unscheduled)


def test_d02_daily_schedule():
    validate_dag(d02_daily_schedule)


def test_d03_with_end_date():
    validate_dag(d03_with_end_date)


def test_d04_time_delta():
    validate_dag(d04_time_delta)


def test_d05_query_with_dates():
    validate_dag(d05_query_with_dates)


def test_d06_templated_query():
    validate_dag(d06_templated_query)


def test_d07_templated_query_ds():
    validate_dag(d07_templated_query_ds)


def test_d08_templated_path():
    validate_dag(d08_templated_path)


def test_d09_no_catchup():
    validate_dag(d09_no_catchup)


def test_d10_non_atomic_send():
    validate_dag(d10_non_atomic_send)


def test_d11_atomic_send():
    validate_dag(d11_atomic_send)


def test_fetch_events():
    events_api_host = 'localhost'
    events_api_port = '5000'
    start_date = "2019-01-01"
    end_date = "2019-01-03"
    fetch_events = BashOperator(
        task_id="fetch_events",
        bash_command=(
            "mkdir -p data/output/events && "
            f"curl -o data/output/events.json http://{events_api_host}:{events_api_port}/events?start_date={start_date}&end_date={end_date}"
        )
    )
    fetch_events.execute({})


def test_calculate_stats():
    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats,
        op_kwargs=dict(
            input_path="data/input/events.json",
            output_path="data/output/stats1.csv"
        ),
    )
    calculate_stats.execute({})


def test_calculate_stats2():
    # use context instead of kwargs
    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats2,
        templates_dict=dict(
            input_path="data/input/events.json",
            output_path="data/output/stats1.csv"
        )
    )
    calculate_stats.execute({})
