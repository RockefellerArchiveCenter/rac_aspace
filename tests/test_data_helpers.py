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
            archival_object (dict): an ArchivesSpace archival object

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
            top_container (dict): an archivespace top container

        Returns:
            bool: Boolean. True if the top_container string matches expected output and type.
        """
        top_container = {'container_type': 'box', 'indicator': '1'}
        result = format_container(top_container)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'box 1')

    def test_format_resource_id(self):
        """
        Checks whether the function returns a concatenated string as expected.

        Args:
            resource (dict): an ArchivesSpace object.

            separator (str): a string separator that will be added in between each section.

        Returns:
            bool: Boolean. True if the top_container string matches expected output and type.
        """
        separator = ":"
        resource = {'id_0': 'FA', 'id_1': '01', 'id_2': '02', 'id_3': '03'}
        result = format_resource_id(resource, separator)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'FA:01:02:03')


    def test_text_in_note(self):
        """
        Checks whether the query string and note content are close to a match.

        Args:
            note (dict): an ArchivesSpace note object

            query_string (str): a string object used to check against note content

        Returns:
            bool: True if the sort ratio is greater than or equal to 97.
        """
        CONFIDENCE_RATIO = 97
        """int: Minimum confidence ratio to match against."""
        note = {"jsonmodel_type": "note_singlepart",
                "type": "langmaterial",
                "content": ["New York Mets"],
                "publish": true }
        query_string = "new York Mets"
        result = text_in_note(note, query_string)
        self.assertTrue(result >= 97)


    def test_get_expression(self):
        """
        Tests whether the date expression function works as intended.

        Args:
            date (dict): an ArchivesSpace date object

        Returns:
            bool: Returns true if the function creates the expected string output.
        """
        date1 = {"expression": "1905 - 1980",
                "date_start": "1905",
                "date_end": "1980",
                "date_type": "inclusive",
                "label": "creation",
                "jsonmodel_type": "date"
                }
        date2 = {"date_start": "1905",
                "date_end": "1980",
                "date_type": "inclusive",
                "label": "creation",
                "jsonmodel_type": "date"
                }
        result1 = get_expression(date1)
        result2 = get_expression(date2)
        self.assertEqual(result1, "1905 - 1980")
        self.assertEqual(result2, "1905 - 1980")

if __name__ == '__main__':
    unittest.main()
