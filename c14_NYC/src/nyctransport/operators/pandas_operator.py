import logging

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class PandasOperator(BaseOperator):
    template_fields = (
        "_input_callable_kwargs",
        "_transform_callable_kwargs",
        "_output_callable_kwargs",
    )

    @apply_defaults
    def __init__(
            self,
            input_callable,
            output_callable,
            transform_callable=None,
            input_callable_kwargs=None,
            transform_callable_kwargs=None,
            output_callable_kwargs=None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        # Attributes for reading data
        self._input_callable = input_callable
        self._input_callable_kwargs = input_callable_kwargs or {}

        # Attributes for transformations
        self._transform_callable = transform_callable
        self._transform_callable_kwargs = transform_callable_kwargs or {}

        # Attributes for writing data
        self._output_callable = output_callable
        self._output_callable_kwargs = output_callable_kwargs or {}

    def execute(self, context):
        logging.info("start execute")
        logging.info("check for transformations")
        not_callable = self._transform_callable is None
        is_single_callable = hasattr(self._transform_callable, '__call__')
        is_multiple_callable = isinstance(self._transform_callable, list)
        logging.debug(f"not_callable = {not_callable}")
        logging.debug(f"is_single_callable = {is_single_callable}")
        logging.debug(f"is_multiple_callable = {is_multiple_callable}")

        logging.info("start reading DataFrame")
        df = self._input_callable(**self._input_callable_kwargs)
        logging.info(f"done reading DataFrame shape={df.shape}")

        if not_callable:
            logging.info("cannot transform DataFrame")

        elif is_single_callable:
            logging.info("start transforming DataFrame")
            df = self._transform_callable(df, **self._transform_callable_kwargs)
            logging.info(f"done transforming DataFrame shape={df.shape}")

        elif is_multiple_callable:
            for call in self._transform_callable:
                logging.info("start transforming DataFrame")
                df = call(df, **self._transform_callable_kwargs)
                logging.info(f"done transforming DataFrame shape={df.shape}")

        logging.info("start writing output")
        self._output_callable(df, **self._output_callable_kwargs)
        logging.info("done writing output")
        logging.info("done execute")
