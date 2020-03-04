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

        Args:
            archival_object: a dictionary with key value pairs

        Returns:
            bool: Boolean. True if locations exists and is not empty. False if empty or doesn't exist
            bool: Boolean. True if locations is a list. False if any other data type.
        """
        archival_object = {'a': 'b'}
        locations = get_locations(archival_object)
        self.assertTrue(locations)
        self.assertIsInstance(locations, list)

    def test_format_container(self):
        """
        Checks whether the function returns a string as expected.
        Need to write a way to get the resource container information from AS.

        Args:
            top_container: a dictionary with key value pairs

        Returns:
            bool: Boolean. True if the top_container string matches expected output. False otherwise.
        """
        top_container = {'container_type': 'box', 'indicator': '1'}
        result = format_container(top_container)
        self.assertEqual(result, 'Box 1')


if __name__ == '__main__':
    unittest.main()
