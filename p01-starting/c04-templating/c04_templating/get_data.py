from datetime import datetime, timedelta
from urllib import request


def determine_y_m_d_h(context):
    try:
        execution_date = context["execution_date"]
        year, month, day, hour, *_ = execution_date.timetuple()
    except KeyError:
        try:
            year = context["year"]
            month = context["month"]
            day = context["day"]
            hour = context["hour"]
        except KeyError:
            execution_date = datetime.utcnow() - timedelta(hours=24)
            year, month, day, hour, *_ = execution_date.timetuple()
    return day, hour, month, year


def _get_data(**context):
    day, hour, month, year = determine_y_m_d_h(context)
    filename = f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    dirname = f"{year}/{year}-{month:0>2}"
    output_path_default = f"/tmp/{dirname}/{filename}"
    output_path = context.get("output_path", output_path_default)
    url = f"https://dumps.wikimedia.org/other/pageviews/{dirname}/{filename}"
    print(f"url = {url}")
    request.urlretrieve(url, output_path)


def _get_data2(year, month, day, hour, output_path, **_):
    """
    same as _get_data, except using templated op_kwargs
    """
    filename = f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    dirname = f"{year}/{year}-{month:0>2}"
    url = f"https://dumps.wikimedia.org/other/pageviews/{dirname}/{filename}"
    print(f"url = {url}")
    request.urlretrieve(url, output_path)
