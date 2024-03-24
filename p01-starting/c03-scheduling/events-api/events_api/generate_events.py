from datetime import timedelta

import pandas as pd

from events_api.generate_events_for_day import _generate_events_for_day


def _generate_events(end_date):
    """Generates a fake dataset with events for 30 days before end date."""

    events = pd.concat(
        [
            _generate_events_for_day(date=end_date - timedelta(days=(30 - i)))
            for i in range(30)
        ],
        axis=0,
    )

    return events
