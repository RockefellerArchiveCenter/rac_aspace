"""
Unit tests for Data Helpers
"""
import unittest


from rac_aspace.data_helpers import get_locations, format_container


class TestDataHelpers(unittest.TestCase):
    """
    Tests the data helper functions.
    """

    def test_get_locations(self):
        """
        Checks whether the function returns a list and if it is empty.
        Need to write a way to get the archival_object information from AS.
        """
        archival_object = {'a': 'b'}
        locations = get_locations(archival_object)
        self.assertTrue(locations)
        self.assertIsInstance(locations, list)

    def test_format_container(self):
        """
        Checks whether the function returns a string as expected.
        Need to write a way to get the resource container information from AS.
        """
        top_container = {'container_type': 'box', 'indicator': '2'}
        result = format_container(top_container)
        self.assertEqual(result, 'Box 1')


if __name__ == '__main__':
    unittest.main()
