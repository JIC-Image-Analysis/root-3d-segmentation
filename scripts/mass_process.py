"""Mass process data in sequential fashion."""

import argparse

from setup_image_data import unpack_series_in_single_file, unpack_all_series_in_directory
from analyse_series import analyse_file

def in_memory(input_file, output_directory):

    backend_dir, process_list = unpack_series_in_single_file(input_file, output_directory)
    for fpath, series, output_path in process_list:
        analyse_file(fpath, output_path, series, backend_dir)


def bash_script(input_file, output_directory):
    backend_dir, process_list = unpack_all_series_in_directory(input_file, output_directory)
    for fpath, series, output_path in process_list:
        cmd = ["python",
               "scripts/analyse_series.py",
               fpath,
               str(series),
               output_directory]
        print(" ".join(cmd))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('input_file', help='Path to input image file')
    parser.add_argument('output_directory', help='Path to output directory for analysis.')
    parser.add_argument('type', choices=["bash-script", "in-memory-python"])

    args = parser.parse_args()

    if args.type == "in-memory-python":
        in_memory(args.input_file, args.output_directory)
    elif args.type == "bash-script":
        bash_script(args.input_file, args.output_directory)

if __name__ == "__main__":
    main()
