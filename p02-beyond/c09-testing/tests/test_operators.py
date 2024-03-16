from airflow.models import Connection
from airflow.operators.bash import BashOperator

from airflowbook.hooks.MovielensHook import MovielensHook
from airflowbook.operators.MovielensPopularityOperator import MovielensPopularityOperator


def test_example():
    result = BashOperator(task_id="hi", bash_command="echo 'hello!'", do_xcom_push=True).execute(context={})
    assert result == "hello!"


def test_movielenspopularityoperator(mocker):
    mock_get = mocker.patch.object(
        target=MovielensHook,
        attribute="get_connection",
        return_value=Connection(conn_id="test", login="airflow", password="airflow")
    )
    assert mock_get.call_count == 0

    task = MovielensPopularityOperator(
        task_id="test_id",
        conn_id="test",
        start_date="2015-01-01",
        end_date="2015-01-03",
        top_n=5,
    )
    result = task.execute(context={})
    assert len(result) == 5
    assert mock_get.call_count == 1
    mock_get.assert_called_with("test")
