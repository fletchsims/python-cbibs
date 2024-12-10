from cbibs.buoy import Cbibs, InvalidStationCodeError, InvalidInputError
import unittest


class TestCbibs(unittest.TestCase):
    def setUp(self):
        self.cbibs = Cbibs(api_key="dummy_key")

    def test_valid_station(self):
        self.cbibs._validate_station("AN")  # Should not raise error

    def test_invalid_station(self):
        with self.assertRaises(InvalidStationCodeError):
            self.cbibs._validate_station("XX")

    def test_iso8601_validation(self):
        self.cbibs._validate_iso8601("2024-12-10T00:00:00Z")  # Should not raise error

    def test_invalid_iso8601(self):
        with self.assertRaises(InvalidInputError):
            self.cbibs._validate_iso8601("invalid-date")
