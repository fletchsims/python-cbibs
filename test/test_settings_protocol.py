from cbibs.buoy import Cbibs

buoy = Cbibs('abcd')
buoy_xml = Cbibs('abcd', resp_type='xml')


# Check that the base url is being correctly generated
def test_settings_protocol():
    assert buoy.url == 'https://mw.buoybay.noaa.gov/api/v1/json/'
    assert buoy_xml.url == 'https://mw.buoybay.noaa.gov/api/v1/xml/'
