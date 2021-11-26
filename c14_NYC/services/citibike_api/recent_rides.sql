SELECT
tripduration,
starttime + INTERVAL '{year_offset} YEARS' AS starttime,
stoptime + INTERVAL '{year_offset} YEARS' AS stoptime,
start_station_id,
start_station_name,
start_station_latitude,
start_station_longitude,
end_station_id,
end_station_name,
end_station_latitude,
end_station_longitude
from tripdata
WHERE stoptime + interval '{year_offset} YEARS' <= NOW()
AND stoptime + interval '{year_offset} YEARS' >= NOW() - interval '{amount} {period}s';