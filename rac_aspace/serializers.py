import csv


class Serializer:

    def __init__(self, filename, filemode="w"):
        """Sets initial attributes for serializers.

        Ensures that a filemode is provided which supports write operations, and
        replaces the filename extension if it does not match the extension
        specified by the class.

        Args:
            filename (str): a filename at which the data should be serialized.
            filemode (str): Optional argument used when opening files.
        """
        if filemode.startswith("r"):
            raise TypeError("Filemode must allow write operations.")
        self.filemode = filemode
        extension = filename.split(".")[-1]
        if extension != self.extension:
            if len(filename.split(".")) > 1:
                filename = filename[:-len(extension)] + self.extension
            else:
                filename = "{}.{}".format(filename, self.extension)
        self.filename = filename

    def write_data(self, data):
        """Writes data to a Serializer class.

        Args:
            data (dict or list): a sequence of dicts.
        """
        fieldnames = list(
            data.keys() if isinstance(
                data, dict) else data[0].keys())
        with open(self.filename, self.filemode) as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)


class CSVWriter(Serializer):
    """Writes data to a CSV file."""

    delimiter = ","
    extension = "csv"


class TSVWriter(Serializer):
    """Writes data to a TSV file."""

    delimiter = "\t"
    extension = "tsv"
