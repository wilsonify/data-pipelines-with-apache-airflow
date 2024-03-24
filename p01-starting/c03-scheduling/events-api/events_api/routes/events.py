from flask import request, abort, jsonify, current_app

from events_api.maybe_str_to_datetime import maybe_str_to_datetime


def events():
    print("events")
    start_date_from_request = request.args.get("start_date", None)
    print(f"start_date_from_request = {start_date_from_request}")
    start_date_dt = maybe_str_to_datetime(start_date_from_request)
    if start_date_dt is None:
        # Check for invalid dates
        # Return 400 with helpful message if dates are invalid
        abort(400, f"Invalid date format. start_date={start_date_dt} must be provided in YYYY-MM-DD format.")

    end_date_from_request = request.args.get("end_date", None)
    end_date_dt = maybe_str_to_datetime(end_date_from_request)
    if end_date_dt is None:
        # Check for invalid dates
        # Return 400 with helpful message if dates are invalid
        abort(400, f"Invalid date format. end_date={end_date_dt} must be provided in YYYY-MM-DD format.")

    events = current_app.config.get("events")
    events = events.loc[events["date"] >= start_date_dt]
    events = events.loc[events["date"] < end_date_dt]
    return jsonify(events.to_dict(orient="records"))
