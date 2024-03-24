from datetime import date

from flask import Flask

from events_api.generate_events import _generate_events
from events_api.routes.events import events

app = Flask(__name__)
app.config["events"] = _generate_events(end_date=date(year=2019, month=1, day=5))
app.add_url_rule('/events', 'events', events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
