from unittest.mock import MagicMock

import pytest
from airflow import DAG
from airflow.models import Connection
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pytest_mock import MockFixture

from airflowbook.hooks.MovielensHook import MovielensHook
from airflowbook.operators import MovielensDownloadOperator, MovielensToPostgresOperator


def test_movielens_download_operator():
    # Mock necessary dependencies
    mock_conn = Connection(conn_id='testconn', login='airflow', password='airflow', host='example.com')
    mock_hook = MagicMock()
    mock_hook.get_ratings.return_value = [{"user_id": 1, "movie_id": 1, "rating": 5},
                                          {"user_id": 2, "movie_id": 2, "rating": 4}]

    # Instantiate the operator
    operator = MovielensDownloadOperator(
        task_id='test_task',
        conn_id='testconn',
        start_date='2015-01-01',
        end_date='2015-01-03',
        output_path='output_path'
    )

    # Set the hook on the operator
    operator.get_hook = MagicMock(return_value=mock_hook)

    # Call the execute method
    operator.execute(context={})


def test_movielens_to_postgres_operator(mocker: MockFixture, test_dag: DAG, postgres, postgres_credentials):
    mocker.patch.object(
        target=MovielensHook,
        attribute="get_connection",
        return_value=Connection(conn_id="test", login="airflow", password="airflow")
    )
    mocker.patch.object(
        target=PostgresHook,
        attribute="get_connection",
        return_value=Connection(
            conn_id="postgres",
            conn_type="postgres",
            host="localhost",
            login=postgres_credentials.username,
            password=postgres_credentials.password,
            port=postgres.ports["5432/tcp"][0],
        ),
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
        dag=test_dag,
    )
    pg_hook = PostgresHook()
    row_count = pg_hook.get_first("SELECT COUNT(*) FROM movielens")[0]
    assert row_count == 0
    pytest.helpers.run_airflow_task(task, test_dag)
    row_count = pg_hook.get_first("SELECT COUNT(*) FROM movielens")[0]
    assert row_count > 0


