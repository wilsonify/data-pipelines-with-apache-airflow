

def print_context(**context):
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
    start = context.get("execution_date","unknown")
    end = context.get("next_execution_date","unknown")
    print(f"Start: {start}, end: {end}")
    print(context)





