"""
Unit tests for Data Helpers
"""
import json
import os
import unittest

import vcr
from asnake.aspace import ASpace
from asnake.jsonmodel import JSONModelObject, wrap_json_object
from rac_aspace import data_helpers

rac_vcr = vcr.VCR(
    serializer="json",
    cassette_library_dir=os.path.join("fixtures", "cassettes"),
    record_mode="once",
    match_on=["path", "method"],
    filter_query_parameters=["username", "password"],
    filter_headers=["Authorization", "X-ArchivesSpace-Session"],
)


class TestDataHelpers(unittest.TestCase):
    """Tests the data helper functions."""

    def obj_from_fixture(self, filename, client=None):
        with open(os.path.join("fixtures", filename)) as json_file:
            data = json.load(json_file)
            obj = wrap_json_object(data, client=client)
            return obj

    def load_fixture(self, filename, client=None):
        with open(os.path.join("fixtures", filename)) as json_file:
            data = json.load(json_file)
            return data

    def test_get_note_text(self):
        """Checks whether the returned note text matches the selected query string."""
        for fixture, expected in [
                ("note_bibliography.json", [
                    "bibliography", "item 1", "item 2"]),
                ("note_index.json", ["title1", "title2"]),
                ("note_multi.json", ["materials are restricted"]),
                ("note_multi_chronology.json", [
                    "general note with chronology", "date", "event1", "event2"]),
                ("note_multi_defined.json", [
                    "bioghist with defined list", "item", "1", "item", "2"]),
                ("note_multi_ordered.json", [
                    "Bioghist with ordered list", "item1", "item2"]),
                ("note_single.json", ["Go Mets!"])]:
            note = self.load_fixture(fixture)
            result = data_helpers.get_note_text(note)
            self.assertTrue(result, list)
            self.assertEqual(
                set(result), set(expected),
                "{} returned {}, expecting {}".format(fixture, result, expected))

    def test_text_in_note(self):
        """Checks whether the query string and note content are close to a match."""
        for fixture, query_string, outcome in [
            ("note_single.json", "Go Mets!", True),
            ("note_single.json", "hello", False),
            ("note_multi.json", "materials are restricted", True),
            ("note_multi.json", "Boo Yankees", False)
        ]:
            note = self.load_fixture(fixture)
            result = data_helpers.text_in_note(note, query_string)
            self.assertEqual(result, outcome)

    def test_object_locations(self):
        """Checks whether the function returns a list of JSONModelObjects."""
        with rac_vcr.use_cassette("test_get_locations.json"):
            repository = ASpace(
                baseurl="http://localhost:8089").repositories(2)
            archival_object = repository.archival_objects(7)
            locations = data_helpers.object_locations(archival_object)
            self.assertIsInstance(locations, list)
            self.assertEqual(len(locations), 1)
            for obj in locations:
                self.assertIsInstance(obj, JSONModelObject)

    def test_format_resource_id(self):
        """Checks whether the function returns a concatenated string as expected."""
        for fixture, formatted, separator in [
                ("archival_object.json", "1;2;3;4", ";"),
                ("archival_object_2.json", "1:2:3", None)]:
            resource = self.load_fixture(fixture)
            if not separator:
                result = data_helpers.format_resource_id(resource)
            else:
                result = data_helpers.format_resource_id(resource, separator)
            self.assertIsInstance(result, str)
            self.assertEqual(result, formatted)

    def test_closest_value(self):
        with rac_vcr.use_cassette("test_closest_value.json"):
            repository = ASpace(
                baseurl="http://localhost:8089").repositories(2)
            archival_object = repository.archival_objects(7)
            value = data_helpers.closest_value(archival_object, "extents")
            self.assertTrue(len(value) > 0)

    def test_get_orphans(self):
        with rac_vcr.use_cassette("test_get_orphans.json"):
            repository = ASpace(
                baseurl="http://localhost:8089").repositories(2)
            archival_objects = repository.archival_objects
            orphans = data_helpers.get_orphans(
                archival_objects, "linked_agents")
            for o in orphans:
                self.assertIsInstance(o, JSONModelObject)

    def test_get_expression(self):
        """Tests whether the date expression function works as intended."""
        files = ["date_expression.json",
                 "date_no_expression.json",
                 "date_no_expression_no_end.json"]
        for f in files:
            date = self.load_fixture(f)
            result = data_helpers.get_expression(date)
            self.assertTrue(result, "1905-1980")

    def test_indicates_restriction(self):
        """Tests whether rights statements are correctly parsed for restrictions."""
        for fixture, restriction_acts, outcome in [
                ("rights_statement_restricted.json",
                 ["disallow", "conditional"], True),
                ("rights_statement_restricted.json", ["allow"], False),
                ("rights_statement_open.json",
                 ["disallow", "conditional"], False),
                ("rights_statement_open.json", ["allow"], False),
                ("rights_statement_conditional.json",
                 ["disallow", "conditional"], True),
                ("rights_statement_conditional.json", ["allow"], False),
                ("rights_statement_not_restricted.json",
                 ["disallow", "conditional"], False),
                ("rights_statement_not_restricted.json", ["allow"], True)]:
            statement = self.load_fixture(fixture)
            status = data_helpers.indicates_restriction(
                statement, restriction_acts)
            self.assertEqual(
                status, outcome,
                "Restriction status for {} expected {}, got {} instead".format(
                    fixture, outcome, status))

    def test_is_restricted(self):
        """Tests whether the function can find restrictions in an AS archival object."""
        for fixture, query_string, restriction_acts, outcome in [
            ("archival_object.json", "materials are restricted",
             ["disallow", "conditional"], True),
            ("archival_object.json",
             "materials are restricted", ["allow"], True),
            ("archival_object.json", "test", ["allow"], False),
            ("archival_object_2.json", "materials are restricted",
             ["disallow", "conditional"], True),
            ("archival_object_2.json", "test", ["allow"], False),
            ("archival_object_3.json",
             "materials are restricted", ["allow"], False)
        ]:
            archival_object = self.load_fixture(fixture)
            result = data_helpers.is_restricted(
                archival_object, query_string, restriction_acts)
            self.assertEqual(result, outcome)

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
        for fixture, format_string in [
            ("date_expression.json", "{begin} - {end} ({expression})"),
            ("date_expression.json", None),
        ]:
            date = self.obj_from_fixture(fixture)
            if not format_string:
                with self.assertRaises(Exception) as excpt:
                    data_helpers.format_from_obj(date, format_string)
                self.assertEqual(
                    "No format string provided.", str(
                        excpt.exception))
            else:
                formatted = data_helpers.format_from_obj(
                    date, format_string)
                self.assertEqual(formatted, "1905 - 1980 (1905-1980)")
                with self.assertRaises(KeyError) as excpt:
                    formatted = data_helpers.format_from_obj(
                        date, "{start} - {end} ({expression})")
                self.assertIn(
                    "was not found in this object", str(
                        excpt.exception))


if __name__ == "__main__":
    unittest.main()
