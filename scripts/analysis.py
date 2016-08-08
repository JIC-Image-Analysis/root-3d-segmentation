"""root-3d-segmentation analysis."""

import os
import json
import logging
import argparse

import numpy as np

from jicbioimage.core.image import Image3D
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite, DataManager, FileBackend
from jicbioimage.segment import SegmentedImage

from segment import segment

__version__ = "0.0.1"

AutoName.prefix_format = "{:03d}_"


def get_data_manager(output_directory):
    """Return FileBackend instance."""
    backend_dir = os.path.join(output_directory, '.backend')
    if not os.path.isdir(backend_dir):
        os.mkdir(backend_dir)
    backend = FileBackend(backend_dir)
    return DataManager(backend)


@transformation
def convert_stack_slices_from_rgb_to_monochrome(stack):
    """Return monochrome Image3D stack from rgb stack.

    This is needed as the version of bfconvert in docker image
    produces TIFF files that have a colour map in them. This is
    expanded by freeimage to produce z-slices with three layers
    in them.
    """
    ydim, xdim, zdim = stack.shape
    data = []
    for zi in range(zdim):
        if zi % 3 == 0:
            data.append(stack[:, :, zi])
    return np.dstack(data).view(Image3D)


def write_segmentation_summary_data(output_filename, segmented_stack):
    """Write JSON description of each segmented cell in a segmented image
    stack."""

    summary_data = []

    for identifier in segmented_stack.identifiers:
        segment = segmented_stack.region_by_identifier(identifier)
        area = int(segment.area)
        centroid = map(float, segment.centroid)

        datum = {"area" : area,
                 "centroid" : centroid,
                 "identifier" : int(identifier)}
        summary_data.append(datum)

    with open(output_filename, "w") as f:
        json.dump(summary_data, f)


def analyse_series(microscopy_collection, series, output_directory):
    logging.info("Analysing series: {}".format(series))
    stack = microscopy_collection.zstack(s=series, c=1)
    stack = convert_stack_slices_from_rgb_to_monochrome(stack)
    stack = segment(stack)
    output_directory = output_directory +  \
                       "series{}-segmented.stack".format(series)
    stack.to_directory(output_directory)
    json_data_filename = os.path.join(output_directory,
            "series{}-cellinfo.json".format(series))
    write_segmentation_summary_data(json_data_filename, stack.view(SegmentedImage))


def analyse_file(fpath, output_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    data_manager = get_data_manager(output_directory)
    microscopy_collection = data_manager.load(fpath)

    fname = os.path.basename(fpath)
    name, ext = os.path.splitext(fname)

    for s in microscopy_collection.series:
        analyse_series(microscopy_collection, s,
                       os.path.join(output_directory, name))

        # To speed up debugging.
        break


def analyse_all_series(input_directory, output_directory):
    """Analyse all the files in a directory."""
    logging.info("Analysing files in directory: {}".format(input_directory))
    for fname in os.listdir(input_directory):
        fpath = os.path.join(input_directory, fname)
        analyse_file(fpath, output_directory)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_source", help="Input file/directory")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Write out intermediate images")
    args = parser.parse_args()

    # Create the output directory if it does not exist.
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    AutoName.directory = args.output_dir

    # Only write out intermediate images in debug mode.
    if not args.debug:
        AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = os.path.join(args.output_dir, log_fname)
    logging_level = logging.INFO
    if args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))

    # Run the analysis.
    if os.path.isfile(args.input_source):
        analyse_file(args.input_source, args.output_dir)
    else:
        parser.error("{} not a file or directory".format(args.input_source))

if __name__ == "__main__":
    main()
