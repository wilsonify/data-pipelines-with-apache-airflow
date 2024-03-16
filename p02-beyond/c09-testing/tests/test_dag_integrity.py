"""Import DAG files and check for DAG objects"""

from airflow.models import DAG
from airflow.utils.dag_cycle_tester import test_cycle as check_for_cycles

from dags import (
    bash_operator_no_command,
    dag_cycle,
    duplicate_task_ids, testme
)


def test_bash_operator_no_command():
    module_vars = vars(bash_operator_no_command)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_dag_cycle():
    module_vars = vars(dag_cycle)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            print(var)
            check_for_cycles(var)


def test_duplicate_task_ids():
    module_vars = vars(duplicate_task_ids)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            check_for_cycles(var)


def test_testme():
    module_vars = vars(testme)
    module_values = module_vars.values()
    for var in module_values:
        if isinstance(var, DAG):
            assert var
            check_for_cycles(var)
