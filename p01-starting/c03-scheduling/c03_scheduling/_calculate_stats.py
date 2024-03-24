import os
from os.path import split
from pathlib import Path

import pandas as pd

from c03_scheduling._email_stats import _print_stats


def create_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False)
    except IOError:
        print("could not save csv, try to make parent directory and retry")
        output_head, output_tail = split(output_path)
        os.makedirs(output_head, exist_ok=True)
        df.to_csv(output_path, index=False)


def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    create_csv(stats, output_path)


def _calculate_stats2(**context):
    """
    same as _calculate_stats, uses context instead of key word arguments

    example input from templated context
    ```
    context = { 'templates_dict':
        { 'input_path': '/data/events/{{ds}}.json', 'output_path': '/data/stats/{{ds}}.csv' }
    }
    ```

    """
    print(f"kwargs = {context}")
    input_path = context["templates_dict"]["input_path"]
    output_path = context["templates_dict"]["output_path"]
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)


def _calculate_stats3(**context):
    """
    Calculates event statistics.
    Warning, this is not atomic,
    if stats is partial, a notification will still be sent.
    """
    input_path = context["templates_dict"]["input_path"]
    output_path = context["templates_dict"]["output_path"]
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    create_csv(stats, output_path)
    _print_stats(stats, email="user@example.com")
