import csv
import json
from os.path import splitext, split

from airflow.models import BaseOperator


class JsonToCsvOperator(BaseOperator):
    def __init__(self, input_path, output_dir, **kwargs):
        super().__init__(**kwargs)
        input_root, input_ext = splitext(input_path)
        input_head, input_tail = split(input_root)
        assert input_ext == ".json", "input must be .json"
        self._input_path = input_path
        self._input_dir = input_head
        self._output_dir = output_dir
        self._output_path = f"{output_dir}/{input_tail}.csv"

    @staticmethod
    def write_json(input_data, input_path):
        with open(input_path, "w") as f:
            f.write(json.dumps(input_data))

    @staticmethod
    def read_csv(path_to_csv):
        with open(path_to_csv, "r") as f:
            reader = csv.DictReader(f)
            result = [dict(row) for row in reader]
        return result

    def read_json(self):
        with open(self._input_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def write_csv(self, data):
        columns = {key for row in data for key in row.keys()}
        with open(self._output_path, mode="w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)

    def execute(self, context):
        data = self.read_json()
        self.write_csv(data)
