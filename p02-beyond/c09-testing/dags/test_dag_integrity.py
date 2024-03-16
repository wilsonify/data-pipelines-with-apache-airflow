"""Import DAG files and check for DAG objects"""

from airflow.models import DAG

import bash_operator_no_command
import dag_cycle
import duplicate_task_ids
import testme


def test_bash_operator_no_command():
    for var in vars(bash_operator_no_command).values():
        if isinstance(var, DAG):
            assert var
            var.test_cycle()


def test_dag_cycle():
    for var in vars(dag_cycle).values():
        if isinstance(var, DAG):
            assert var
            var.test_cycle()


def test_duplicate_task_ids():
    for var in vars(duplicate_task_ids).values():
        if isinstance(var, DAG):
            assert var
            var.test_cycle()


def test_testme():
    for var in vars(testme).values():
        if isinstance(var, DAG):
            assert var
            var.test_cycle()
