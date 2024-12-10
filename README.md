# python-cbibs
Python module to interact with the CBIBS API.

- [CBIBS](https://www.buoybay.noaa.gov/)
- [API Documentation](https://www.buoybay.noaa.gov/data/api)

## Installation ##
To get the package, execute:
```shell
pip install cbibs
```

## Usage ##
View the CBIBS API documentation on [CBIBS](https://www.buoybay.noaa.gov/data/api). By default the response output will 
be in JSON format. If you would like XML, configure your instance to use XML (see example below).

Then set up an CBIBS instance, set your API key, and make any available requests.

```python
from cbibs.buoy import Cbibs

# Create CBIBS instance
buoy = Cbibs(api_key='API_KEY')
buoy_xml = Cbibs(api_key='API_KEY', response_format='xml')

# Get all current readings from all stations
latest_all = buoy.get_current_readings_all_stations()

# Get the latest station readings from AN
station_readings = buoy.get_station_readings('AN')

# Query a specific station with parameters
station_variable = buoy.query_station(
    station_name="AN",
    start_date='2020-04-01T10:00:00z',
    end_date='2020-04-01T20:00:00z',
    variable="sea_water_temperature"
)
```