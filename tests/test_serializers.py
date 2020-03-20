"""
Unit tests for Serializers
"""
import csv
import unittest
from os import remove
from os.path import isfile

from rac_aspace import serializers


class TestSerializers(unittest.TestCase):
    """Tests CSV and TSV serializers."""

    def setUp(self):
        """Sets data attributes to be serialized."""
        self.long_data = [{"column1": "value", "column2": "value"},
                          {"column1": "another value", "column2": "blah"}]
        self.short_data = [{"column1": "value", "column2": "value"}]

    def test_csv_serializer(self):
        """Tests CSVWriter.

        Ensures that the correct filename is created, and that the expected
        number of rows are written to the file.
        """
        expected_filepath = "spreadsheet.csv"
        for filepath in ["spreadsheet.csv", "spreadsheet",
                         "spreadsheet.tsv", "spreadsheet.jpeg"]:
            for data in [self.long_data, self.short_data]:
                serializer = serializers.CSVWriter(filepath)
                serializer.write_data(data)
                with open(expected_filepath, "r") as out_file:
                    reader = csv.reader(
                        out_file, delimiter=serializer.delimiter)
                    out_data = [r for r in reader]
                    self.assertEqual(set(out_data[0]), set(
                        ["column1", "column2"]))
                    self.assertEqual(len(out_data), len(data) + 1)
                remove(expected_filepath)

    def test_tsv_serializer(self):
        """Tests TSVWriter.

        Ensures that the correct filename is created, and that the expected
        number of rows are written to the file.
        """
        expected_filepath = "spreadsheet.tsv"
        for filepath in ["spreadsheet.tsv", "spreadsheet",
                         "spreadsheet.csv", "spreadsheet.jpeg"]:
            for data in [self.long_data, self.short_data]:
                serializer = serializers.TSVWriter(filepath)
                serializer.write_data(data)
                with open(expected_filepath, "r") as out_file:
                    reader = csv.reader(
                        out_file, delimiter=serializer.delimiter)
                    out_data = [r for r in reader]
                    self.assertEqual(out_data[0], ["column1", "column2"])
                    self.assertEqual(len(out_data), len(data) + 1)
                remove(expected_filepath)

    def test_filemodes(self):
        """Tests different filemodes.

        Ensures that write modes create a file, and that read-only modes throw
        a meaningful exception.
        """
        for filemode in ["a", "a+", "w", "w+"]:
            for serializer in [serializers.CSVWriter, serializers.TSVWriter]:
                expected_filepath = "test.{}".format(serializer.extension)
                s = serializer("test", filemode=filemode)
                s.write_data(self.short_data)
                self.assertTrue(isfile(expected_filepath))
                remove(expected_filepath)
        for filemode in ["r", "r+"]:
            for serializer in [serializers.CSVWriter, serializers.TSVWriter]:
                with self.assertRaises(TypeError):
                    serializer("test", filemode=filemode)

    def tearDown(self):
        for filename in ["spreadsheet.csv", "spreadsheet.tsv"]:
            if isfile(filename):
                remove(filename)


if __name__ == '__main__':
    unittest.main()
