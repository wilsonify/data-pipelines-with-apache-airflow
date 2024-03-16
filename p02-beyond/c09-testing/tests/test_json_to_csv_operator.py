import csv
import errno
import json
import os

from airflowbook.operators.operators.JsonToCsvOperator import JsonToCsvOperator


def remove_without_errors(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Ignore error if file does not exist
            raise  # Re-raise any other OSError


def write_input_json(input_data, input_path):
    with open(input_path, "w") as f:
        f.write(json.dumps(input_data))


def read_output_csv(output_path):
    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        result = [dict(row) for row in reader]
    return result


def test_json_to_csv_operator():
    fake_input_data = json.load(open(f"{os.path.dirname(__file__)}/data/fake_input.json"))
    write_input_json(fake_input_data, "input.json")
    strat = JsonToCsvOperator(task_id="test", input_path="input.json", output_path="output.csv")
    strat.execute(context={})
    result = read_output_csv("output.csv")
    assert result == fake_input_data
    remove_without_errors("input.json")
    remove_without_errors("output.csv")
