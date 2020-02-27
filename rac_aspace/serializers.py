import argparse
import csv


class Serializer:

    def __init__(self, filename, filemode="w"):
        self.filename = filename
        self.fieldnames = list(data.keys())
        self.data = data
        self.delimiter = delimiter

    def run(self):
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(
                f, fieldnames=self.fieldnames, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(data)


class CSVWriter(Serializer):

    delimiter = "','"


class TSVWriter(Serializer):

    delimiter = "'\t'"


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        help="The desired name of your output file.")
    return parser


data = {}
fieldnames = []
delimiter = ''
parser = get_parser()
args = parser.parse_args()
filename = args.filename


def main():
    if '.csv' in filename:
        write = CSVWriter(filename, data)
        write.run()
    else:
        write = TSVWriter(filename, data)
        write.run()


if __name__ == "__main__":
    main()
