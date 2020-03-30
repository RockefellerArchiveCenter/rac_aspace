"""
Unit tests for Data Helpers
"""
import json
import os
import unittest

from asnake.jsonmodel import wrap_json_object
from rac_aspace import data_helpers


class TestDataHelpers(unittest.TestCase):
    """Tests the data helper functions."""

    def obj_from_fixture(self, filename):
        with open(os.path.join("fixtures", filename)) as json_file:
            data = json.load(json_file)
            return wrap_json_object(data)

    def test_get_note_text(self):
        """Checks whether the returned note text matches the selected query string."""
        note = self.obj_from_fixture("note_multi.json")
        result = data_helpers.get_note_text(note)
        self.assertTrue(result, list)
        self.assertEqual(result, ["materials are restricted"])

    def test_text_in_note(self):
        """Checks whether the query string and note content are close to a match."""
        query_string = "New York Mets"
        note = self.obj_from_fixture("note_single.json")
        result = data_helpers.text_in_note(note, query_string)
        self.assertTrue(result)

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

    def test_format_resource_id(self):
        """Checks whether the function returns a concatenated string as expected."""
        separator = ":"
        resource = self.obj_from_fixture("archival_object.json")
        result = data_helpers.format_resource_id(resource, separator)
        self.assertIsInstance(result, str)
        self.assertEqual(result, '1:2:3:4')

    def test_closest_value(self):
        pass

    def test_get_orphans(self):
        pass

    def test_get_expression(self):
        """Tests whether the date expression function works as intended."""
        files = ['date_expression.json', 'date_no_expression.json']
        for f in files:
            date = self.obj_from_fixture(f)
            result = data_helpers.get_expression(date)
            self.assertTrue(result, "1905-1980")

    def test_associated_objects(self):
        pass

    def test_indicates_restriction(self):
        """Tests whether rights statements are correctly parsed for restrictions."""
        for fixture, outcome in [
                ("rights_statement_restricted.json", True),
                ("rights_statement_open.json", False),
                ("rights_statement_conditional.json", True)]:
            statement = self.obj_from_fixture(fixture)
            status = data_helpers.indicates_restriction(statement)
            self.assertEqual(
                status, outcome,
                "Restriction status for {} expected {}, got {} instead".format(
                    fixture, outcome, status))

    def test_is_restricted(self):
        """Tests whether the function can find restrictions in an AS archival object."""
        archival_object = self.obj_from_fixture("archival_object.json")
        result = data_helpers.is_restricted(archival_object)
        self.assertEqual(result, True)
        """
        Cannot currently test the restrictions portion because data helper is unwritten
        """

    def test_strip_html_tags(self):
        """Ensures HTML tags are correctly removed from strings."""
        input = "<h1>Title</h1><p>This is <i>some</i> text! It is wrapped in a variety of html tags, which should <strong>all</strong> be stripped &amp; not returned.</p>"
        expected = "TitleThis is some text! It is wrapped in a variety of html tags, which should all be stripped &amp; not returned."
        output = data_helpers.strip_html_tags(input)
        self.assertEqual(
            expected, output,
            "Expected string {} but got {} instead.".format(expected, output))

    def test_format_from_obj(self):
        """Test that format strings can be passed to objects as expected."""
        date = self.obj_from_fixture("date_expression.json")
        formatted = data_helpers.format_from_obj(
            date, "{begin} - {end} ({expression})")
        self.assertEqual(formatted, "1905 - 1980 (1905-1980)")
        with self.assertRaises(KeyError) as excpt:
            formatted = data_helpers.format_from_obj(
                date, "{start} - {end} ({expression})")
        self.assertIn("was not found in this object", str(excpt.exception))


if __name__ == '__main__':
    unittest.main()
