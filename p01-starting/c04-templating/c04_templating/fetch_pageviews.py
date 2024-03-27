def construct_pageview_dict(pagenames):
    result = dict.fromkeys(pagenames, 0)
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title] = view_counts
    return result


def save_query_to_file(execution_date, result):
    with open("/tmp/postgres_query.sql", "w") as f:
        for pagename, pageviewcount in result.items():
            line = f"INSERT INTO pageview_counts VALUES ('{pagename}', {pageviewcount}, '{execution_date}');\n"
            f.write(line)


def _fetch_pageviews(pagenames):
    """
    example result
    {'Facebook': '778', 'Apple': '20', 'Google': '451', 'Amazon': '9', 'Microsoft': '119'}
    """
    result = construct_pageview_dict(pagenames)
    print(result)


def _fetch_pageviews2(pagenames, execution_date, **_):
    result = construct_pageview_dict(pagenames)
    save_query_to_file(execution_date, result)
