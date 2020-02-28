"""
Unit tests for Data Helpers
"""
import unittest


from rac_aspace.data_helpers import get_locations


class TestDataHelpers(unittest.TestCase):
    """
    Tests the data helper functions.
    """

    def test_get_locations(self):
        archival_object = {'a': 'b'}
        locations = get_locations(archival_object)
        self.assertTrue(locations)
        self.assertIsInstance(locations, list)


if __name__ == '__main__':
    unittest.main()
