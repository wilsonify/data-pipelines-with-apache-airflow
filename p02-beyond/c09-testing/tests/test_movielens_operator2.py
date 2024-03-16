from datetime import datetime

import pytest
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook

from airflowbook.operators.MovielensToPostgresOperator import MovielensToPostgresOperator


def test_movielens_to_postgres_operator():
    dag2 = DAG(
        dag_id="test_dag",
        default_args={"owner": "airflow", "start_date": datetime(2015, 1, 1)},
        schedule_interval="@daily",
    )
    task = MovielensToPostgresOperator(
        task_id="test",
        movielens_conn_id="movielens_id",
        start_date="{{ prev_ds }}",
        end_date="{{ ds }}",
        postgres_conn_id="postgres_id",
        insert_query=(
            "INSERT INTO movielens (movieId,rating,ratingTimestamp,userId,scrapeTime) "
            "VALUES ({0}, '{{ macros.datetime.now() }}')"
        ),
        dag=dag2,
    )

    pg_hook = PostgresHook()

    row_count = pg_hook.get_first("SELECT COUNT(*) FROM movielens")[0]
    assert row_count == 0

    pytest.helpers.run_airflow_task(task, dag2)

    row_count = pg_hook.get_first("SELECT COUNT(*) FROM movielens")[0]
    assert row_count > 0
