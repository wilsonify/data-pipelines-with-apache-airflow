from datetime import datetime

import pytest

from events_api.__main__ import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    with app.test_client() as client:
        yield client


def test_events_without_parameters(client):
    """Test /events endpoint without parameters."""
    # Providing valid dates to the endpoint
    response = client.get('/events')
    assert response.status_code == 400


def test_events_with_valid_parameters(client):
    """Test /events endpoint with valid parameters."""
    start_date = '2019-01-01'
    end_date = '2019-01-03'
    expected_start = datetime.strptime(start_date, '%Y-%m-%d').date()
    expected_end = datetime.strptime(end_date, '%Y-%m-%d').date()
    response = client.get('/events?start_date=2019-01-01&end_date=2019-01-03')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert data[:3] == [
        {"date": "Tue, 01 Jan 2019 00:00:00 GMT", "user": "211.101.7.158"},
        {"date": "Tue, 01 Jan 2019 00:00:00 GMT", "user": "170.116.8.25"},
        {"date": "Tue, 01 Jan 2019 00:00:00 GMT", "user": "62.68.154.180"}
    ]
    for event in data:
        assert 'user' in event
        assert 'date' in event
        # Adjust the date format for comparison
        obs_start = datetime.strptime(event['date'], '%a, %d %b %Y %H:%M:%S GMT').date()
        obs_end = datetime.strptime(event['date'], '%a, %d %b %Y %H:%M:%S GMT').date()
        assert obs_start >= expected_start
        assert obs_end < expected_end


def test_events_with_missing_dates(client):
    """Test /events endpoint with invalid dates."""
    response = client.get('/events')
    assert response.status_code == 400


def test_events_with_invalid_dates(client):
    """Test /events endpoint with invalid dates."""
    response = client.get('/events?start_date=invalid_date&end_date=invalid_date')
    assert response.status_code == 400
