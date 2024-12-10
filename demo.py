import os

from dotenv import load_dotenv

from cbibs.buoy import Cbibs

load_dotenv()
API_KEY = os.getenv('API_KEY')
buoy = Cbibs(api_key=API_KEY)

latest_all = buoy.get_current_readings_all_stations()
station_readings = buoy.get_station_readings('AN')
station_variable = buoy.query_station(
    station_name="AN",
    start_date='2020-04-01T10:00:00z',
    end_date='2020-04-01T20:00:00z',
    variable="sea_water_temperature"
)
