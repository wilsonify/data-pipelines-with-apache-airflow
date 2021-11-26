with
citibike as (
    select
    start_location_id,
    end_location_id,
    date_part('dow', stoptime) as weekday,
    CASE WHEN extract(hour from stoptime) >= 8 and extract(hour from stoptime) < 11 THEN '8 AM - 11 AM'
         WHEN extract(hour from stoptime) >= 11 and extract(hour from stoptime) < 16 THEN '11 AM - 4 PM'
         WHEN extract(hour from stoptime) >= 16 and extract(hour from stoptime) < 19 THEN '4 PM - 7 PM'
         WHEN extract(hour from stoptime) >= 19 and extract(hour from stoptime) < 22 THEN '7 PM - 10 PM'
         ELSE '10 PM - 8 AM' END
         AS time_group,
    cast(avg(tripduration) as float) as avg_seconds
    from citi_bike_rides
    where start_location_id != end_location_id
    group by start_location_id, end_location_id, weekday, time_group
    ),
taxi as (
    select
    start_location_id,
    end_location_id,
    date_part('dow', stoptime) as weekday,
    CASE WHEN extract(hour from stoptime) >= 8 and extract(hour from stoptime) < 11 THEN '8 AM - 11 AM'
         WHEN extract(hour from stoptime) >= 11 and extract(hour from stoptime) < 16 THEN '11 AM - 4 PM'
         WHEN extract(hour from stoptime) >= 16 and extract(hour from stoptime) < 19 THEN '4 PM - 7 PM'
         WHEN extract(hour from stoptime) >= 19 and extract(hour from stoptime) < 22 THEN '7 PM - 10 PM'
         ELSE '10 PM - 8 AM' END
         AS time_group,
    cast(avg(tripduration) as float) as avg_seconds
    from taxi_rides
    where start_location_id != end_location_id
    group by start_location_id, end_location_id, weekday, time_group
    )
select
citibike.start_location_id,
citibike.end_location_id,
citibike.weekday,
citibike.time_group,
citibike.avg_seconds as citibike_avg_seconds,
taxi.avg_seconds as taxi_avg_seconds,
case when citibike.avg_seconds < taxi.avg_seconds then 'Citi Bike'
     when taxi.avg_seconds < citibike.avg_seconds then 'Taxi'
     else 'No difference' end
     as fastest
from citibike inner join taxi
on citibike.start_location_id=taxi.start_location_id
and citibike.end_location_id=taxi.end_location_id
and citibike.weekday=taxi.weekday
and citibike.time_group=taxi.time_group
order by start_location_id, end_location_id, weekday, time_group;