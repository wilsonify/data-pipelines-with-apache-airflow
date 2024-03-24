def _print_context(**kwargs):
    """
    example context
    {
     'dag': <DAG: print_context>,
     'ds': '2019-07-04',
     'next_ds': '2019-07-04',
     'next_ds_nodash': '20190704',
     'prev_ds': '2019-07-03',
     'prev_ds_nodash': '20190703',
     ...
    }
    """
    print(kwargs)

def _print_context2(**context):
    print(context)


def _print_context3(**context):
    # Prints e.g.:
    # Start: 2019-07-13T14:00:00+00:00, end: 2019-07-13T15:00:00+00:00
    start = context["execution_date"]
    end = context["next_execution_date"]
    print(f"Start: {start}, end: {end}")


