"""CBIBS Module"""
import requests

DEFAULT_DOMAIN = 'mw.buoybay.noaa.gov'


class CbibsApiError(Exception):
    """Base class for all errors/exceptions"""


class Cbibs:
    def __init__(self, key, protocol='https', domain=DEFAULT_DOMAIN, ver='v1', type='json'):
        """Constructor"""
        self.key = key
        if protocol and protocol not in ('http', 'https'):
            protocol = 'https'
        self.url = protocol + "://" + domain + '/api/' + ver + '/'

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, *args):
        self.session.close()
        self.session = None
        return False

    def buoy(self, query, **kwargs):
        pass
