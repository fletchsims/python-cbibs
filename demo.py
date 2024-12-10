import os
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

from cbibs.buoy import Cbibs

load_dotenv()
API_KEY = os.getenv('API_KEY')
buoy = Cbibs(api_key=API_KEY)
buoy_xml = Cbibs(api_key=API_KEY, response_format='xml')

latest_all_xml = buoy_xml.get_current_readings_all_stations()
station_readings = buoy.get_station_readings('AN')
station_variable = buoy.query_station(
    station_name="AN",
    start_date='2020-04-01T10:00:00z',
    end_date='2020-04-01T20:00:00z',
    variable="sea_water_temperature"
)

print('Printing XML Version')
ET.indent(latest_all_xml)
print(ET.tostring(latest_all_xml, encoding='unicode'))

print('Printing JSON Version')
print(station_readings)