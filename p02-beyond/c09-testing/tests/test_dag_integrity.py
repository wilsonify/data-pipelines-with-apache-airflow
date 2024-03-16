"""Test integrity of DAGs."""

import glob
import importlib.util
import os

from pytest import mark
from airflow.models import DAG

path_to_dags = f"{os.path.dirname(__file__)}/../dags"
DAG_PATH = f"{path_to_dags}/**.py"
DAG_FILES = glob.glob(DAG_PATH)


@mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    """Import DAG files and check for DAG."""
    dag_file_root, dag_file_ext = os.path.splitext(dag_file)
    dag_file_head, dag_file_tail = os.path.split(dag_file_root)
    mod_spec = importlib.util.spec_from_file_location(name=dag_file_tail, location=dag_file_head)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)
    for var in vars(module).values():
        if isinstance(var, DAG):
            assert var
            var.test_cycle()
