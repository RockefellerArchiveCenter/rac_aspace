"""
Unit tests for Data Helpers
"""
import unittest
import os

from rac_aspace.data_helpers import (get_locations, format_container,
                                     format_resource_id)


class TestDataHelpers(unittest.TestCase):
    """
    Tests the data helper functions.
    """

    # @mock.patch('get_locations')
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

        Args:
            top_container: a dictionary with key value pairs

        Returns:
            bool: Boolean. True if the top_container string matches expected output. False otherwise.
        """
        top_container = {'container_type': 'box', 'indicator': '1'}
        result = format_container(top_container)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'box 1')

    def test_format_resource_id(self):
        """

        """
        separator = ":"
        resource = {'id_0': 'FA', 'id_1': '01', 'id_2': '02', 'id_3': '03'}
        result = format_resource_id(resource, separator)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'FA:01:02:03')


if __name__ == '__main__':
    unittest.main()
