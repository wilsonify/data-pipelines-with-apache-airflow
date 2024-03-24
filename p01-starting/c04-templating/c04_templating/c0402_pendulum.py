
"""
# Pendulum behavior equal to native Python datetime

The Wikipedia pageviews URL requires zero-padded months, days, and hours (e.g.,
“07” for hour 7). Within the Jinja-templated string we therefore apply string format-
ting for padding:
{{ '{:02}'.format(execution_date.hour) }}


Which arguments are templated?
It is important to know not all operator arguments can be templates! Every operator
can keep an allowlist of attributes that can be made into templates. By default, they
are not, so a string {{ name }} will be interpreted as literally {{ name }} and not tem-
plated by Jinja, unless included in the list of attributes that can be templated. This
list is set by the attribute template_fields on every operator. You can check these
attributes in the documentation (https://airflow.apache.org/docs); go to the operator
of your choice and view the template_fields item.
Note the elements in template_fields are names of class attributes. Typically,
the argument names provided to __init__ match the class attributes names, so
everything listed in template_fields maps 1:1 to the __init__ arguments. How-
ever, technically it’s possible they don’t, and it should be documented as to which
class attribute an argument maps.
"""


from datetime import datetime
import pendulum
datetime.now().year
# 2020
pendulum.now().year
# 2020


