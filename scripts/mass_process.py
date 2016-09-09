"""Mass process data in sequential fashion."""

import argparse

from setup_image_data import unpack_series_in_single_file
from analyse_series import analyse_file

def mass_process_file(input_file, output_directory):

    backend_dir, process_list = unpack_series_in_single_file(input_file, output_directory)

    print(process_list)

    for fpath, series, output_path in process_list:
        analyse_file(fpath, output_path, series, backend_dir)
        break

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('input_file', help='Path to input image file')
    parser.add_argument('output_directory', help='Path to output directory for analysis.')

    args = parser.parse_args()

    mass_process_file(args.input_file, args.output_directory)

if __name__ == "__main__":
    main()
