from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from dags import d01_umbrella


def test_d01_umbrella():
    module_vars = vars(d01_umbrella)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_fetch_weather_forecast():
    strat = DummyOperator(task_id="fetch_weather_forecast")
    strat.execute({})


def test_fetch_sales_data():
    strat = DummyOperator(task_id="fetch_sales_data")
    strat.execute({})


def test_clean_forecast_data():
    strat = DummyOperator(task_id="clean_forecast_data")
    strat.execute({})


def test_clean_sales_data():
    strat = DummyOperator(task_id="clean_sales_data")
    strat.execute({})


def test_join_datasets():
    strat = DummyOperator(task_id="join_datasets")
    strat.execute({})


def test_train_ml_model():
    strat = DummyOperator(task_id="train_ml_model")
    strat.execute({})


def test_deploy_ml_model():
    strat = DummyOperator(task_id="deploy_ml_model")
    strat.execute({})
