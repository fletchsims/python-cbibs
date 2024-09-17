from cbibs.buoy import Cbibs

buoy = Cbibs('abcd', 'https')


# Check that the base url is being correctly generated
def test_settings_protocol():
    assert buoy.url == 'https://mw.buoybay.noaa.gov/api/v1/'
