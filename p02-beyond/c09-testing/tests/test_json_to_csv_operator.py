import csv
import json
import os

from airflowbook.operators.JsonToCsvOperator import JsonToCsvOperator


def write_input_json(input_data, input_path):
    with open(input_path, "w") as f:
        f.write(json.dumps(input_data))


def read_output_csv(output_path):
    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        result = [dict(row) for row in reader]
    return result


def test_json_to_csv_operator():
    expected_output_list = read_output_csv(f"{os.path.dirname(__file__)}/data/expected_output/fake_input.csv")

    strat = JsonToCsvOperator(
        task_id="test",
        input_path=f"{os.path.dirname(__file__)}/data/input/fake_input.json",
        output_dir=f"{os.path.dirname(__file__)}/data/output"
    )
    strat.execute(context={})

    result = read_output_csv(f"{os.path.dirname(__file__)}/data/output/fake_input.csv")

    assert result == expected_output_list
