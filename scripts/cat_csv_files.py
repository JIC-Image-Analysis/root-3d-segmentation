"""Script to concatenate all the csv output from top level analysis directory.

Assumes analysis directory has the structure below:

timepoint_directory/series_directory/cells.csv
"""

import argparse
import os
import os.path

from csv import header


def print_csv(directory):
    csv_path = os.path.join(directory, "cells.csv")
    if os.path.isfile(csv_path):
        with open(csv_path, "r") as fh:
            print(fh.read())



def process_timepoint_directory(directory):
    series_paths = [os.path.join(directory, d)
                    for d in os.listdir(directory)]
    for s in series_paths:
        print_csv(s)


def process_top_directory(directory):
    print(header())
    timepoints_paths = [os.path.join(directory, d)
                        for d in os.listdir(directory)
                        if not d.endswith(".lif")  \
                        and not d.startswith(".")]
    for t in timepoints_paths:
        process_timepoint_directory(t)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    args = parser.parse_args()
    process_top_directory(args.directory)

if __name__ == "__main__":
    main()
