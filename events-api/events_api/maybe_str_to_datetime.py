from datetime import datetime


def maybe_str_to_datetime(value):
    try:
        result = datetime.strptime(value, "%Y-%m-%d")
    except:
        result = None
    return result
