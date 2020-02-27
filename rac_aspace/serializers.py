import csv


data = {}


class Serializer:

    def __init__(self, filename, filemode="w"):
        """
        Currently this class expects to get the following parameters:
        Filename: a filename including the file extension
        Data: Data in a dictionary. Doesn't handle nested arrays.
        Filemode: Optional argument set to work with already existing files.
        """
        self.filename = filename
        self.fieldnames = list(data.keys())
        self.data = data

    def write_data(self, data):
        """
        This function writes the data passed to it to a csv or tsv.
        """
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(
                f, fieldnames=self.fieldnames, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)


class CSVWriter(Serializer):

    delimiter = "','"


class TSVWriter(Serializer):

    delimiter = "'\t'"
