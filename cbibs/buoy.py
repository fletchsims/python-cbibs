"""CBIBS Module"""
import requests

DEFAULT_DOMAIN = 'mw.buoybay.noaa.gov'


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
    def __init__(self, key, protocol='https', domain=DEFAULT_DOMAIN, ver='v1', data_type='json'):
        """Constructor"""
        self.key = key
        if protocol and protocol not in ('http', 'https'):
            protocol = 'https'
        self.url = f"{protocol}://{domain}/api/{ver}/{data_type}/"

    def __enter__(self):
        """Enter the method."""
        self.session = requests.Session()
        return self

    def __exit__(self, *args):
        """Exit the method and clean up."""
        self.session.close()
        self.session = None
        return False

    def buoy(self, query, **kwargs):
        pass
