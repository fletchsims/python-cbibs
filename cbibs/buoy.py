"""CBIBS Module"""
import requests

DEFAULT_DOMAIN = 'mw.buoybay.noaa.gov'

__endpoints__ = ["json", "xml"]


class CbibsApiError(Exception):
    """Base class for all errors/exceptions."""


class InvalidInputError(CbibsApiError):
    """
    There is a problem with the input the user provided.
    - Bad value
    - Invalid API Key
    """


class UnknownError(CbibsApiError):
    """There is a problem with CBIBS server."""


class Cbibs:
    def __init__(self, key, protocol='https', domain=DEFAULT_DOMAIN, ver='v1', resp_type='json'):
        """Constructor"""
        self.key = key
        if protocol and protocol not in ('http', 'https'):
            protocol = 'https'
        self.resp_type = resp_type
        self.url = f"{protocol}://{domain}/api/{ver}/{resp_type}/"

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
        if self.session:
            response = self.session.get(self.url)
        else:
            response = requests.get(self.url)
        if response.status_code != requests.codes.ok:
            raise CbibsApiError

        return self._parse_response(response)

    def _parse_response(self, resp):
        """Parse the response based on the data type (JSON or XML)"""
        if self.resp_type == 'json':
            return resp.json()
        elif self.resp_type == 'xml':
            # Parse XML and return ElementTree object
            return ET.fromstring(resp.text)
        else:
            raise ValueError(f"Unsupported data type: {self.resp_type}")

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

