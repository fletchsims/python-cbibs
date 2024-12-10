"""CBIBS Module"""
import xml.etree.ElementTree as et

import requests
from dateutil.parser import isoparse
from requests.adapters import HTTPAdapter
from urllib3 import Retry

BASE_URL = 'https://mw.buoybay.noaa.gov/api'
SUPPORTED_FORMATS = {'json', 'xml'}
DEFAULT_TIMEOUT = 10
__endpoints__ = ["station", "query"]
STATIONS = frozenset({'UP', 'GR', 'J', 'FL', 'SR', 'PL', 'AN', 'YS', 'N', 'SN', 'S'})
COMMON_PARAMETERS = frozenset({
    'air_pressure', 'air_temperature', 'wind_speed', 'wind_speed_of_gust', 'wind_from_direction', 'relative_humidity',
    'latitude_decimal', 'longitude_decimal', 'sea_water_temperature', 'sea_water_electrical_conductivity',
    'mml_avg_nitrates', 'simple_turbidity', 'seanettle_prob', 'mass_concentration_of_chlorophyll_in_sea_water',
    'mass_concentration_of_oxygen_in_sea_water', 'sea_water_salinity', 'sea_surface_wind_wave_period',
    'wave_direction_spread', 'sea_surface_wave_from_direction', 'sea_surface_wave_significant_height',
    'sea_surface_wave_mean_height', 'all'
})


class CbibsError(Exception):
    """Base class for all errors/exceptions."""

    def __init__(self, message='An error occurred with the CBIBS API'):
        self.message = message
        super().__init__(self.message)


class InvalidInputError(CbibsError):
    """There is a problem with the input the user provided."""

    def __init__(self, input_value):
        self.input_value = input_value
        message = f'Invalid input: {self.input_value}'
        super().__init__(message)


class NotAuthorizedError(CbibsError):
    """The API Key is invalid or not authorized."""

    def __init__(self, message='Invalid or not authorized API Key. You may have entered it incorrectly.'):
        self.message = message
        super().__init__(message)


class InvalidStationCodeError(CbibsError):
    """The user used an invalid station code in the GET request."""

    def __init__(self, input_value):
        self.input_value = input_value
        message = (f'{self.input_value} is an invalid station code. The station code must be one of the following: '
                   f'UP, GR, J, FL, SR, PL, AN, YS, N, SN, S')
        super().__init__(message)


class UnknownError(CbibsError):
    """There is a problem with CBIBS server."""

    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        message = f'Unknown error with CBIBS API (status code: {self.status_code}: {self.response_text}'
        super().__init__(message)


class Cbibs:
    def __init__(self, api_key, url=BASE_URL, version='v1', response_format='json'):
        """Constructor"""
        self.api_key = api_key
        self.response_format = response_format
        self.version = version
        self.url = f"{url}/{version}/{response_format}"
        self.session = None

    def __enter__(self):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        return self

    def __exit__(self, *args):
        """Exit the method and clean up."""
        self.session.close()
        self.session = None
        return False

    def get_current_readings_all_stations(self):
        url = f'{self.url}/station'
        response = self._make_request(url)
        return self._parse_response(response)

    def query_station(self, station_name: str,
                      start_date: str,
                      end_date: str,
                      variable: str):
        """
        Query data from a specific station with optional parameters.

        :param station_name: The station name (e.g., 'AN').
        :param start_date: Start date and time in ISO 8601 format (e.g., '2020-04-01T10:00:00z').
        :param end_date: End date and time in ISO 8601 format (e.g., '2020-04-01T20:00:00z').
        :param variable: The variable to query (e.g., 'sea_water_temperature').
        :return: Parsed API response.
        """

        self._validate_station(station_name)
        if start_date:
            self._validate_iso8601(start_date)
        if end_date:
            self._validate_iso8601(end_date)
        if variable and variable not in COMMON_PARAMETERS:
            raise InvalidInputError(f"Invalid variable: {variable}")
        params = {
            "sd": start_date,
            "ed": end_date,
            "var": variable
        }

        url = f"{self.url}/query/{station_name.upper()}"
        response = self._make_request(url, params=params)
        return self._parse_response(response)

    def get_station_readings(self, station_name: str):
        """
        Query data from a specific station with optional parameters.

        :param station_name: The station name (e.g., 'AN').
        :return: Parsed API response.
        """

        self._validate_station(station_name)
        url = f"{self.url}/station/{station_name.upper()}"
        response = self._make_request(url)
        return self._parse_response(response)

    def _validate_station(self, station_name: str):
        if station_name.upper() not in STATIONS:
            raise InvalidStationCodeError(station_name)

    def _make_request(self, url: str, params: dict = None):
        """
        Make the GET request to the given URL.

        :param url: URL to make the GET request to
        :param params: Parameters to pass to the GET request.
        :return: response object
        """
        if params is None:
            params = {}
        else:
            params = params.copy()

        params['key'] = self.api_key

        if self.session:
            response = self.session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        else:
            response = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise
        return response

    def _parse_response(self, resp):
        """
        Parse the response based on the data type (JSON or XML). The CBIBS API does not throw a 400 when
        an invalid API key is used for XML response type (throws a 200 (OK) for JSON).

        :param resp: requests.Response
        :return: JSON or XML response
        """
        if self.response_format == 'json':
            json_response = resp.json()
            if 'error' in json_response and json_response["error"] == 'Invalid API Key':
                raise NotAuthorizedError
            else:
                return json_response
        elif self.response_format == 'xml':
            return et.fromstring(resp.text)
        else:
            raise ValueError(f"Unsupported response format: {self.response_format}")

    def _validate_iso8601(self, date_str):
        try:
            isoparse(date_str)
        except ValueError:
            raise InvalidInputError(f"Invalid ISO 8601 date: {date_str}")
