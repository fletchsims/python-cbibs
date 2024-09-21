"""CBIBS Module"""
import requests
import xml.etree.ElementTree as et

from requests.auth import HTTPBasicAuth

BASE_URL = 'https://mw.buoybay.noaa.gov/api/v1'
__endpoints__ = ["station", ""]
STATIONS = ['UP', 'GR', 'J', 'FL', 'SR', 'PL', 'AN', 'YS', 'N', 'SN', 'S']


class CbibsApiError(Exception):
    """Base class for all errors/exceptions."""
    def __init__(self, message='An error occurred with the CBIBS API'):
        self.message = message
        super().__init__(self.message)


class InvalidInputError(CbibsApiError):
    """There is a problem with the input the user provided."""
    def __init__(self, input_value):
        self.input_value = input_value
        message = f'Invalid input: {self.input_value}'
        super().__init__(message)


class UnknownError(CbibsApiError):
    """There is a problem with CBIBS server."""
    def __init__(self, status_code, response_text):
        self.status_code = status_code
        self.response_text = response_text
        message = f'Unknown error with CBIBS API (status code: {self.status_code}: {self.response_text}'
        super().__init__(message)


class Cbibs:
    session = None

    def __init__(self, api_key, url=BASE_URL, response_format='json'):
        """Constructor"""
        self.api_key = api_key
        self.response_format = response_format
        self.url = f"{url}/{response_format}"

    def __enter__(self):
        """Enter the method."""
        self.session = requests.Session()
        return self

    def __exit__(self, *args):
        """Exit the method and clean up."""
        self.session.close()
        self.session = None
        return False

    def get_latest_measurements_all_stations(self):
        url = f'{self.url}/station'
        try:
            response = self._make_request(url)
            return self._parse_response(response)
        except requests.RequestException as e:
            raise CbibsApiError

    def get_latest_measurements_one_station(self, name):
        """
        Gets the latest measurements for a single station from CBIBS. Name needs to be
        in the list of known stations and in all uppercase. Otherwise, function will throw
        an error.

        :param name: The name of the station in all caps.
        :return: API response.
        """
        if name.upper() not in STATIONS:
            raise InvalidInputError(name)
        url = f'{self.url}/station/{name.upper()}'
        try:
            response = self._make_request(url)
            print(response.status_code)
            return self._parse_response(response)
        except requests.RequestException as e:
            raise CbibsApiError(f'Request failed with {e}')

    def _make_request(self, url):
        """
        Make the GET request to the given URL.

        :param url: URL to make the GET request to
        :return: response object
        """
        if self.session:
            response = self.session.get(url, params={'key': self.api_key})
        else:
            response = requests.get(url, params={'key': self.api_key})
        if response.status_code != 200:
            raise CbibsApiError
        return self._parse_response(response)

    def _parse_response(self, resp):
        """
        Parse the response based on the data type (JSON or XML)

        :param resp:
        :return:
        """
        if self.response_format == 'json':
            return resp.json()
        elif self.response_format == 'xml':
            return et.fromstring(resp.text)
        else:
            raise ValueError(f"Unsupported data type: {self.response_format}")

    def buoy(self, query, **kwargs):
        """
        Current/active values for either one station or all stations (xml or json)
        Time based values for either one station or all stations (xml or json)
        Time based values for a specific var for one station or all stations (xml or json)
        :param query:
        :param kwargs:
        :return:
        """
        pass
