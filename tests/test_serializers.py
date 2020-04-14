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

    def check_serializer(self, serializer):
        """Abstract function to test serializers.

        Ensures that the correct filename is created, and that the expected
        number of rows are written to the file."""
        expected_filepath = "spreadsheet.{}".format(serializer.extension)
        for filepath in ["spreadsheet.{}".format(serializer.extension), "spreadsheet",
                         "spreadsheet.csv", "spreadsheet.jpeg"]:
            for data in [self.long_data, self.short_data]:
                loaded = serializer(filepath)
                loaded.write_data(data)
                with open(expected_filepath, "r") as out_file:
                    reader = csv.reader(
                        out_file, delimiter=serializer.delimiter)
                    out_data = [r for r in reader]
                    self.assertEqual(set(out_data[0]), set(
                        ["column1", "column2"]))
                    self.assertEqual(len(out_data), len(data) + 1)
                remove(expected_filepath)

    def test_csv_serializer(self):
        """Tests CSVSerializer."""
        self.check_serializer(serializers.CSVSerializer)

    def test_tsv_serializer(self):
        """Tests TSVSerializer."""
        self.check_serializer(serializers.TSVSerializer)

    def test_filemodes(self):
        """Tests different filemodes.

        Ensures that write modes create a file, and that read-only modes throw
        a meaningful exception.
        """
        for filemode in ["a", "a+", "w", "w+"]:
            for serializer in [serializers.CSVSerializer,
                               serializers.TSVSerializer]:
                expected_filepath = "test.{}".format(serializer.extension)
                s = serializer("test", filemode=filemode)
                s.write_data(self.short_data)
                self.assertTrue(isfile(expected_filepath))
                with self.assertRaises(TypeError):
                    s.read_data()
        for filemode in ["r", "r+"]:
            for serializer in [serializers.CSVSerializer,
                               serializers.TSVSerializer]:
                s = serializer("test", filemode=filemode)
                read = s.read_data()
                self.assertIsInstance(read, list)
                with self.assertRaises(TypeError):
                    s.write_data(self.short_data)
        for filename in ["test.tsv", "test.csv"]:
            remove(filename)

    def test_read_data(self):
        """Tests correct returned from a CSV or TSV file."""
        filename = "read_file.csv"
        fieldnames = list(self.long_data[0].keys())
        with open(filename, "w") as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            writer.writerows(self.long_data)
        read = serializers.CSVSerializer(filename, filemode="r").read_data()
        self.assertIsInstance(read, list)
        self.assertEqual(read, self.long_data)
        remove(filename)

    def tearDown(self):
        for filename in ["spreadsheet.csv", "spreadsheet.tsv"]:
            if isfile(filename):
                remove(filename)


if __name__ == '__main__':
    unittest.main()
