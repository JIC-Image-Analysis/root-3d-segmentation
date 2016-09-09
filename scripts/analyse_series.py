"""root-3d-segmentation analysis."""

import os
import json
import logging
import argparse

from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.segment import SegmentedImage

from setup_image_data import get_data_manager
from utils import ColorImage3D
from segment import segment
from cellinfo import cellinfo
from filter_real_cells import filter_by_property, real_cells
from create_intensity_stack import create_intensity_stack
from csv import csv
from histogram import generate_histogram
from omexml import OmeXml

__version__ = "0.0.1"

AutoName.prefix_format = "{:03d}_"


def create_istack(segmentation, info, output_dir, name):
    istack_fname = name + ".istack"
    istack_output_dir = os.path.join(output_dir, istack_fname)
    segmentation.view(ColorImage3D).to_directory(istack_output_dir)
    info_fpath = os.path.join(istack_output_dir, "cellinfo.json")
    with open(info_fpath, "w") as fh:
        json.dump(info, fh, indent=2)
    return istack_output_dir, info_fpath


def analyse_series(microscopy_collection, input_fname, series, series_name,
                   output_directory):

    # Write series identifier to disk.
    series_id_fname = os.path.join(output_directory, "series_id.txt")
    with open(series_id_fname, "w") as fh:
        fh.write("{}\n".format(series))

    # Write series name to disk.
    series_name_fname = os.path.join(output_directory, "series_name.txt")
    with open(series_name_fname, "w") as fh:
        fh.write("{}\n".format(series_name))

    # Segment root into cells.
    stack = microscopy_collection.zstack(s=series, c=1)
    stack = segment(stack)
    segmented_cells = stack.view(SegmentedImage)
    num_cells = len(segmented_cells.identifiers)
    logging.info("Root segmented into {} cells".format(num_cells))

    # Calculate cell info and write to disk.
    intensity_stack = microscopy_collection.zstack(s=series, c=0)
    info = cellinfo(intensity_stack, segmented_cells)

    # Create segmented istack.
    create_istack(segmented_cells, info, output_directory, "segmented")

    # Filter cells.
    min_cell_size = 10000
    max_cell_size = 80000
    logging.info("Filter cells < {} voxels".format(min_cell_size))
    logging.info("Filter cells > {} voxels".format(max_cell_size))
    filtered_cells, filtered_info = filter_by_property(segmented_cells,
                                                       info,
                                                       real_cells,
                                                       min_cell_size,
                                                       max_cell_size)
    filtered_istack_dir, filtered_info_fpath = create_istack(filtered_cells,
                                                             filtered_info,
                                                             output_directory,
                                                             "filtered")
    num_cells = len(filtered_cells.identifiers)
    logging.info("Post filter {} cells remain".format(num_cells))

    # Create intensity stack.
    create_intensity_stack(filtered_cells,
                           filtered_info,
                           os.path.join(output_directory, "intensity.stack"))

    # Write csv.
    csv_text = csv(input_fname, series_name, series, filtered_info)
    with open(os.path.join(output_directory, "cells.csv"), "w") as fh:
        fh.write(csv_text)

    # Generate histogram.
    hist_fpath = os.path.join(output_directory, "histogram.png")
    return_code = generate_histogram(filtered_info_fpath, hist_fpath)
    if not int(return_code) == 0:
        logging.warning("Failed to generate histogram")
    else:
        logging.info("Generated histogram: {}".format(hist_fpath))


def analyse_file(fpath, output_directory, series, backend_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    logging.info("Series identifier: {}".format(series))
    data_manager = get_data_manager(backend_directory)
    microscopy_collection = data_manager.load(fpath)
    omexml = OmeXml(fpath)

    series_name = omexml.series(series).name
    logging.info("Series name: {}".format(series_name))

    analyse_series(microscopy_collection,
                   os.path.basename(fpath),
                   series,
                   series_name,
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
    backend_dir = args.output_dir

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
    analyse_file(args.input_source, output_dir, args.series, backend_dir)


if __name__ == "__main__":
    main()
