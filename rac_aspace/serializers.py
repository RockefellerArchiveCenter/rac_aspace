import csv


class BaseSerializer:

    def __init__(self, filename, filemode="w"):
        """Sets initial attributes for serializers.

        Ensures that a filemode is provided which supports write operations, and
        replaces the filename extension if it does not match the extension
        specified by the class.

        :param str filename: a filename at which the data should be serialized.
        :param str filemode: Optional argument used when opening files.
        """
        self.filemode = filemode
        extension = filename.split(".")[-1]
        if extension != self.extension:
            if len(filename.split(".")) > 1:
                filename = filename[:-len(extension)] + self.extension
            else:
                filename = "{}.{}".format(filename, self.extension)
        self.filename = filename

    def write_data(self, data):
        """Writes data to a file.

        :param: data (dict or list) a sequence of dicts.
        """
        if self.filemode.startswith("r"):
            raise TypeError("Filemode must allow write operations.")
        fieldnames = list(
            data.keys() if isinstance(
                data, dict) else data[0].keys())
        with open(self.filename, self.filemode) as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)

    def read_data(self):
        if not self.filemode.startswith("r"):
            raise TypeError("Read-only filemode required.")
        with open(self.filename, self.filemode) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]


class CSVSerializer(BaseSerializer):
    """Writes data to a CSV file."""

    delimiter = ","
    extension = "csv"


class TSVSerializer(BaseSerializer):
    """Writes data to a TSV file."""

    delimiter = "\t"
    extension = "tsv"
