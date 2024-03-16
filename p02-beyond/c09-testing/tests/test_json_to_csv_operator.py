import os

from airflowbook.operators.JsonToCsvOperator import JsonToCsvOperator


def test_json_to_csv_operator():
    strat = JsonToCsvOperator(
        task_id="test",
        input_path=f"{os.path.dirname(__file__)}/data/input/fake_input.json",
        output_dir=f"{os.path.dirname(__file__)}/data/output"
    )
    expected_output_list = strat.read_csv(f"{os.path.dirname(__file__)}/data/expected_output/fake_input.csv")
    strat.execute(context={})

    actual_output_list = strat.read_csv(f"{os.path.dirname(__file__)}/data/output/fake_input.csv")

    assert actual_output_list == expected_output_list
