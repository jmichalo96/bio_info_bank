"""
This module contains csv_reader for getting data from content requirement file
and csv_writer for log file.
"""
import csv

# data = [line.strip().split(',') for line in open(file_name)]


URL_COLUMN = 0
REQUIREMENT_STRING_COLUMN = 1
STATUS_CODE = 2
STATUS_MESSAGE = 3
TIME_STAMP = 4
LOAD_TIME = 5
REQUIREMENT_STATUS = 6


def open_file(file):
    try:
        with open(file, newline='') as csv_file:
            data_reader = csv.reader(csv_file)
            headers = next(data_reader)
            data_set = [row for row in data_reader]
        return data_set
    except FileNotFoundError as fnf_error:
        print(fnf_error)


def write_to_log_file(urls_info, log_file_path):
    try:
        with open(log_file_path, 'a', newline='') as log_file:
            for url_row in urls_info:
                log_file.write("URL: " + url_row[URL_COLUMN] + "\n")
                log_file.write("Requirement_string: " + url_row[REQUIREMENT_STRING_COLUMN] + "\n")
                log_file.write("Status code: " + url_row[STATUS_CODE] + "\n")
                log_file.write("Status message: " + url_row[STATUS_MESSAGE] + "\n")
                log_file.write("Last check: " + url_row[TIME_STAMP] + "\n")
                log_file.write("Load time: " + url_row[LOAD_TIME] + "\n")
                log_file.write("Requirement status: OK\n" if url_row[REQUIREMENT_STATUS] == "\u2713" else "Requirement status: NO\n")
                log_file.write(30 * "- -"+"\n")
    except FileNotFoundError as fnf_error:
        print(fnf_error)



