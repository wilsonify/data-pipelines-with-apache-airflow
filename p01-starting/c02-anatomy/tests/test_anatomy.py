from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from c02_anatomy.curl_thespacedevs import curl_command_str
from dags import (

    d0203_Instantiate_DAG,
    d0204_Instantiate_bash_operator,
    d0206_invoking_python_operator,
    d02010_download_rocket_launches
)


def test_d0203_Instantiate_DAG():
    module_vars = vars(d0203_Instantiate_DAG)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_d0204_Instantiate_bash_operator():
    module_vars = vars(d0204_Instantiate_bash_operator)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_d0206_invoking_python_operato():
    module_vars = vars(d0206_invoking_python_operator)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_d02010_download_rocket_launches():
    module_vars = vars(d02010_download_rocket_launches)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_download_launches():
    strat = BashOperator(task_id="download_launches", bash_command=curl_command_str)
    strat.execute({})
