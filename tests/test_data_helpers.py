"""
Unit tests for Data Helpers
"""
import json
import os
import unittest

from asnake.jsonmodel import wrap_json_object
from rac_aspace.data_helpers import (get_locations, format_container,
                                     format_resource_id, text_in_note,
                                     get_expression, get_note_text,
                                     is_restricted)


class TestDataHelpers(unittest.TestCase):
    """
    Tests the data helper functions.
    """

    def test_get_note_text(self):
        """
        """
        with open(os.path.join("fixtures", "note_multi.json"), "r") as json_file:
            data = json.load(json_file)
            note = wrap_json_object(data)
            result = get_note_text(note)
            self.assertTrue(result, list)
            self.assertEqual(result, "materials are restricted")

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
        query_string = "New York Mets"
        """int: Minimum confidence ratio to match against."""
        with open(os.path.join("fixtures", "note_single.json"), "r") as json_file:
            data = json.load(json_file)
            note = wrap_json_object(data)
            result = text_in_note(note, query_string)
            self.assertTrue(result >= CONFIDENCE_RATIO)

    # def test_get_locations(self):
        """
        Data helper as written won't work without AS calls. Container and Location
        information are in different objects, not just Archival Objects.
        """
        # """
        # Checks whether the function returns a list and if it is empty.
        # Need to write a way to get the archival_object information from AS.

        # Args:
        # archival_object (dict): an ArchivesSpace archival object

        # Returns:
        # bool: Boolean. True if locations exists and is not empty.
        # bool: Boolean. True if locations is a list. False if any other data type.
        # """
        # with open(os.path.join("fixtures", "archival_object.json"), "r") as json_file:
        # data = json.load(json_file)
        # archival_object = wrap_json_object(data)
        # locations = get_locations(archival_object)
        # self.assertNotEqual(
        # locations, False,
        # "Get locatins returned an error: {}".format(locations)
        # )
        # self.assertIsInstance(locations, list)

    def test_format_location(self):
        pass

    def test_format_container(self):
        """
        Checks whether the function returns a string as expected.

        Args:
            top_container (dict): an archivespace top container

        Returns:
            bool: Boolean. True if the top_container string matches expected output and type.
        """
        with open(os.path.join("fixtures", "top_container.json"), "r") as json_file:
            data = json.load(json_file)
            top_container = wrap_json_object(data)
            result = format_container(top_container)
            self.assertEqual(result, 'box 1')
            self.assertIsInstance(result, str)

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
        with open(os.path.join("fixtures", "archival_object.json"), "r") as json_file:
            data = json.load(json_file)
            resource = wrap_json_object(data)
            result = format_resource_id(resource, separator)
            self.assertIsInstance(result, str)
            self.assertEqual(result, '1:2:3:4')

    def test_closest_value(self):
        pass

    def test_get_orphans(self):
        pass

    def test_get_expression(self):
        """
        Tests whether the date expression function works as intended.

        Args:
            date (dict): an ArchivesSpace date object

        Returns:
            bool: Returns true if the function creates the expected string output.
        """
        files = ['date_expression.json', 'date_no_expression.json']
        for f in files:
            with open(os.path.join("fixtures", f), "r") as json_file:
                data = json.load(json_file)
                date = wrap_json_object(data)
                result = get_expression(date)
                self.assertTrue(result, "1905-1980")

    def test_associated_objects(self):
        pass

    def test_indicates_restriction(self):
        pass

    def test_is_restricted(self):
        """
        Tests whether the function can find restrictions in an AS archival object.

        Args:
            archival_object (dict): and ArchivesSpace archival object

        Returns:
            bool: Returns true when finding a restriction in a note or rights statement.
        """
        with open(os.path.join("fixtures", "archival_object.json"), "r") as json_file:
            data = json.load(json_file)
            archival_object = wrap_json_object(data)
            result = is_restricted(archival_object)
            self.assertEqual(result, True)
            """
            Cannot currently test the restrictions portion because data helper is unwritten
            """


if __name__ == '__main__':
    unittest.main()
