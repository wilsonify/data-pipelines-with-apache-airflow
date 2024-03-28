import os


def construct_pageview_dict(source, pagenames):
    result = dict.fromkeys(pagenames, 0)
    with open("source", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title] = view_counts
    return result


def save_query_to_file(dest_dir, execution_date, result):
    with open(f"{dest_dir}/postgres_query.sql", "w") as f:
        for pagename, pageviewcount in result.items():
            line = f"INSERT INTO pageview_counts VALUES ('{pagename}', {pageviewcount}, '{execution_date}');\n"
            f.write(line)


def _fetch_pageviews(**context):
    """
    example result
    {'Facebook': '778', 'Apple': '20', 'Google': '451', 'Amazon': '9', 'Microsoft': '119'}
    """
    pagenames = context["pagenames"]
    source_dir = context.get("source_dir", "/tmp/wikipageviews")
    dest_dir = context.get("dest_dir", "/tmp/wikipageviewcounts")

    result = construct_pageview_dict(source_dir, pagenames)
    print(result)


def _fetch_pageviews2(execution_date, **context):
    pagenames = context["pagenames"]
    source_dir = context.get("source_dir", "/tmp/wikipageviews")
    dest_dir = context.get("dest_dir", "/tmp/wikipageviewcounts")
    os.makedirs(dest_dir, exist_ok=True)
    result = construct_pageview_dict(source_dir, pagenames)
    save_query_to_file(execution_date, result)
