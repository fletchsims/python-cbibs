from cbibs.buoy import Cbibs

buoy = Cbibs(api_key='')

# print(buoy.get_latest_measurements_all_stations())

res = buoy.get_station_readings('AN')
from datetime import datetime


def format_date(dt: datetime) -> str:
    """Format datetime to ISO 8601 with lowercase 'z'."""
    return dt.strftime('%Y-%m-%dT%H:%M:%S') + 'z'


start = datetime(2020, 4, 1, 10, 0, 0)
end = datetime(2020, 4, 1, 20, 0, 0)

# Format dates correctly
formatted_start = format_date(start)  # '2020-04-01T10:00:00z'
formatted_end = format_date(end)
response = buoy.query_station(
    station_name="AN",
    start_date=formatted_start,
    end_date=formatted_end,
    variable="sea_water_temperature"
)
