"""Conftest file."""

import datetime
import os
from collections import namedtuple

import pytest
from airflow import DAG
from airflow.models import BaseOperator
from pytest_docker_tools import fetch, container

pytest_plugins = ["helpers_namespace"]

@pytest.helpers.register
def run_airflow_task(task: BaseOperator, dag: DAG):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
        ignore_ti_state=True,
    )


@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={"owner": "airflow", "start_date": datetime.datetime(2015, 1, 1)},
        schedule_interval="@daily",
    )


@pytest.fixture(name="postgres")
def postgres_fixture():
    postgres_image = fetch(repository="postgres:11.1-alpine")
    pgimage_str = "{postgres_image.id}"
    pgenvironment = {"POSTGRES_USER": "{postgres_credentials.username}",
                     "POSTGRES_PASSWORD": "{postgres_credentials.password}", }
    pgport = {"5432/tcp": None}
    pgvol = {
        os.path.join(os.path.dirname(__file__), "postgres-init.sql"): {
            "bind": "/docker-entrypoint-initdb.d/postgres-init.sql"}
    }
    return container(
        image=pgimage_str,
        environment=pgenvironment,
        ports=pgport,
        volumes=pgvol,
    )


@pytest.fixture(scope="module")
def postgres_credentials():
    PostgresCredentials = namedtuple("PostgresCredentials", ["username", "password"])
    return PostgresCredentials("testuser", "testpass")
