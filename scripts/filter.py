"""Find regions that correspond to cells."""

import os
import os.path
import argparse
import json

import numpy as np
import skimage.io

from jicbioimage.core.util.color import identifier_from_unique_color
from jicbioimage.core.image import Image3D, _sorted_listdir
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName


def rgb_to_identifier(array):
    ydim, xdim, zdim = array.shape
    id_array = np.zeros((ydim, xdim), dtype=np.uint64)

    for y in range(ydim):
        for x in range(xdim):
            id_array[y, x] = identifier_from_unique_color(array[y, x])

    return id_array


@transformation
def filter_by_property(im3d, cellinfo, filter_func):
    for i, props in cellinfo.items():
        if not filter_func(props):
            im3d[im3d == int(i)] = 0
    return im3d


def real_cells(cell_properties):
    if cell_properties["area"] < 10000:
        return False
    if cell_properties["area"] > 80000:
        return False
    return True


def stack_from_directory(directory):
    skimage.io.use_plugin('freeimage')

    def is_image_fname(fname):
        "Return True if fname is '.png', '.tif' or '.tiff'."""
        image_exts = set([".png", ".tif", ".tiff"])
        base, ext = os.path.splitext(fname)
        return ext in image_exts
    fnames = [fn for fn in _sorted_listdir(directory)
              if is_image_fname(fn)]
    fpaths = [os.path.join(directory, fn) for fn in fnames]

    images = [rgb_to_identifier(skimage.io.imread(fp)) for fp in fpaths]
    stack = np.dstack(images)
    return stack.view(Image3D)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        parser.error("No such dir: " + args.input_dir)

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    AutoName.directory = args.output_dir

    cellinfo = json.load(file(os.path.join(args.input_dir, "cellinfo.json")))
    cells = stack_from_directory(args.input_dir)

    cells = filter_by_property(cells, cellinfo, real_cells)
