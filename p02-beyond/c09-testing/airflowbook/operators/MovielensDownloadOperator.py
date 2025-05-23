import json

from airflow.models import BaseOperator

from airflowbook.hooks.MovielensHook import MovielensHook


class MovielensDownloadOperator(BaseOperator):
    """
    pulls movie ratings between two given dates,
    which the user can provide via templated variables.
    """
    # list of attributes that can be templated by Jinja.
    template_fields = ("_start_date", "_end_date", "_output_path")

    def __init__(self, conn_id, start_date, end_date, output_path, **kwargs):
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._output_path = output_path

    def execute(self, context):
        with MovielensHook(self._conn_id) as hook:
            ratings = hook.get_ratings(
                start_date=self._start_date,
                end_date=self._end_date,
            )
            for count, batch in enumerate(ratings):
                with open(f"{self._output_path}/{count}.json", "w") as f:
                    f.write(json.dumps(ratings))
