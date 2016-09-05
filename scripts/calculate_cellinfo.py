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
from cellinfo import cellinfo
from filter_real_cells import filter_by_property, real_cells
from omexml import OmeXml

__version__ = "0.0.1"

AutoName.prefix_format = "{:03d}_"


def get_data_manager(output_directory):
    """Return FileBackend instance."""
    backend_dir = os.path.join(output_directory, '.backend')
    if not os.path.isdir(backend_dir):
        os.mkdir(backend_dir)
    backend = FileBackend(backend_dir)
    return DataManager(backend)


def analyse_series(microscopy_collection, series, series_name, output_directory):

    logging.info("Analysing series: {}".format(series))

    # Write series identifier to disk.
    series_id_fname = os.path.join(output_directory, "series_id.txt")
    with open(series_id_fname, "w") as fh:
        fh.write("{}\n".format(series))

    # Write series name to disk.
    series_name_fname = os.path.join(output_directory, "series_name.txt")
    with open(series_name_fname, "w") as fh:
        fh.write("{}\n".format(series_name))

    # Segment root and write to disk.
    seg_out_dir = os.path.join(output_directory, "segmented.istack")
    stack = microscopy_collection.zstack(s=series, c=1)
    stack = segment(stack)
    stack.to_directory(seg_out_dir)

    # Calculate cell info and write to disk.
    cellinfo_fname = os.path.join(seg_out_dir, "cellinfo.json")
    segmented_stack = stack.view(SegmentedImage)
    intensity_stack = microscopy_collection.zstack(s=series, c=0)
    info = cellinfo(intensity_stack, segmented_stack)
    with open(cellinfo_fname, "w") as fh:
        json.dump(info, fh, indent=2)

    # Filter cells.


def analyse_file(fpath, output_directory, series):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    data_manager = get_data_manager(output_directory)
    microscopy_collection = data_manager.load(fpath)
    omexml = OmeXml(fpath)

    series_name = omexml.series(series).name
    analyse_series(microscopy_collection, series, series_name,
                   output_directory)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_source", help="Input file")
    parser.add_argument("series", type=int, help="series identifier")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Write out intermediate images")
    args = parser.parse_args()

    if not os.path.isfile(args.input_source):
        parser.error("{} not a file".format(args.input_source))

    # Create the output directory if it does not exist.
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    # Create output directory for input microscopy file.
    fname = os.path.basename(args.input_source)
    name, ext = os.path.splitext(fname)
    output_dir = os.path.join(args.output_dir, name)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Create output directory for input series.
    output_dir = os.path.join(output_dir, str(args.series))
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Only write out intermediate images in debug mode.
    if not args.debug:
        AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = os.path.join(output_dir, log_fname)
    logging_level = logging.INFO
    if args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))

    # Run the analysis.
    analyse_file(args.input_source, output_dir, args.series)

if __name__ == "__main__":
    main()
