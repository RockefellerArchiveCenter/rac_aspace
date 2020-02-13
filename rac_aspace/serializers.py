import argparse
from configparser import ConfigParser
import csv

file_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), config.get(
        "Destinations", "filename")
)

FILE_TYPE_CHOICES = ["csv", "tsv"]


def open_file(file_path):
    """"Opens file to be written to"""
    if file_type == 'csv':
        writer = csv.writer(open(file_path, 'w'))
    else:
        writer = csv.writer(open(file_path, delimiter='\t'))


def create_headings(column_headings):
    """Creates a spreadsheet with column headings"""
    writer.writerow(column_headings)


def write_data(data):
    """"Writes data to a csv file"""
    for d in data:
        column_data = d.column
        heading_data = d.heading
        writer.writerow([column_data, heading_data])


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_type",
        choices=FILE_TYPE_CHOICES,
        help="The type of file you would like to output data to (tsv or csv)")


parser = get_parser()
args = parser.parse_args()
open_file(file_path)
create_headings([column, headings])
write_data(data)
