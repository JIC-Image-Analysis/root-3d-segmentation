"""root-3d-segmentation analysis."""

import os
import logging
import argparse

from jicbioimage.core.image import Image, Image3D
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite, DataManager, FileBackend

import SimpleITK as sitk

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
def identity(im3d):
    return im3d


@transformation
def filter_median(im3d):
    itk_im = sitk.GetImageFromArray(im3d)
    median_filter = sitk.MedianImageFilter()
    itk_im = median_filter.Execute(itk_im)
    return Image3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


@transformation
def gradient_magnitude(im3d):
    itk_im = sitk.GetImageFromArray(im3d)
    itk_im = sitk.GradientMagnitude(itk_im)
    return Image3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


@transformation
def discrete_gaussian_filter(im3d, variance):
    itk_im = sitk.GetImageFromArray(im3d)
    gaussian_filter = sitk.DiscreteGaussianImageFilter()
    gaussian_filter.SetVariance(2.0)
    itk_im = gaussian_filter.Execute(itk_im)
    return Image3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


@transformation
def morphological_watershed(im3d, level):
    itk_im = sitk.GetImageFromArray(im3d)
    itk_im = sitk.MorphologicalWatershed(itk_im, level=level)
    return Image3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


def analyse_file(fpath, output_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    data_manager = get_data_manager(output_directory)
    microscopy_collection = data_manager.load(fpath)

    stack = microscopy_collection.zstack(c=1)
    stack = identity(stack)
    stack = filter_median(stack)
    stack = gradient_magnitude(stack)
    stack = discrete_gaussian_filter(stack, 2.0)
    stack = morphological_watershed(stack, 250)


def analyse_directory(input_directory, output_directory):
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
    elif os.path.isdir(args.input_source):
        analyse_directory(args.input_source, args.output_dir)
    else:
        parser.error("{} not a file or directory".format(args.input_source))

if __name__ == "__main__":
    main()
