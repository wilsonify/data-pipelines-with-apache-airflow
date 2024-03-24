curl -o /tmp/wikipageviews.gz \
https://dumps.wikimedia.org/other/pageviews/{{ execution_date.year }}/{{ execution_date.year }}-{{ '{:02}'.format(execution_date.month) }}/pageviews-{{ execution_date.year }} {{ '{:02}'.format(execution_date.month) }} \
{{ '{:02}'.format(execution_date.day) }}-{{ '{:02}'.format(execution_date.hour) }}0000.gz