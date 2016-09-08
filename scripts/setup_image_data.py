"""Work out which LIF files need to be unpacked, and unpack them."""

import os
import errno
import argparse

from pprint import pprint

from jicbioimage.core.io import DataManager, FileBackend

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise


def get_data_manager(output_directory):
    """Return FileBackend instance."""

    backend_dir = os.path.join(output_directory, '.backend')
    if not os.path.isdir(backend_dir):
        os.mkdir(backend_dir)
    backend = FileBackend(backend_dir)
    return DataManager(backend)

def is_directory_processed(output_directory):

    return False

def unpack_series_in_single_file(filename, output_directory):
    """Unpack the series contained in a particular image file. Return a list of
    tuples in the form:

    (image_filename, series_identifier, output_path)

    where:

    image_filename is the name of the image file passed in to the function
    series_identifier is the numerical identifier of the series, from 0 onwards
    output_path is target directory for analysed data from the series.
    """

    data_manager = get_data_manager(output_directory)
    microscopy_collection = data_manager.load(filename)

    file_basename = os.path.basename(filename)
    file_output_directory = os.path.join(output_directory, file_basename)

    mkdir_p(file_output_directory)

    process_list = []
    series_ids = microscopy_collection.series
    for sid in series_ids:
        series_name = "series_{}".format(sid)
        series_output_directory = os.path.join(file_output_directory, series_name)
        mkdir_p(series_output_directory)

        if not is_directory_processed(series_output_directory):
            process_list.append((filename, sid, series_output_directory))

    return process_list

def unpack_all_series_in_directory(input_directory, output_directory):
    """Given an input directory, find all of the image files in that directory,
    unpack them, and return a list of files and series to process, together
    with output directories into which processed output should be written."""

    all_input_files = os.listdir(input_directory)

    process_list = []

    for input_filename in all_input_files:
        fq_input_filename = os.path.join(input_directory, input_filename)
        process_commands = unpack_series_in_single_file(fq_input_filename, 
                                                        output_directory)
        process_list += process_commands
 
    return process_list


def main():

    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('input_directory', help='Input directory containing LIF files to unpack')
    parser.add_argument('output_directory', help='Directory into which output should be written')

    args = parser.parse_args()

    process_list = unpack_all_series_in_directory(args.input_directory, args.output_directory)

    pprint(process_list)

if __name__ == '__main__':
    main()