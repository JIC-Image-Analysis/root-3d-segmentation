"""Utility functions."""

import os

import numpy as np
import skimage.io

from jicbioimage.core.util.color import identifier_from_unique_color
from jicbioimage.core.image import Image3D, _sorted_listdir


def rgb_to_identifier(array):
    ydim, xdim, zdim = array.shape
    id_array = np.zeros((ydim, xdim), dtype=np.uint64)

    for y in range(ydim):
        for x in range(xdim):
            id_array[y, x] = identifier_from_unique_color(array[y, x])

    return id_array


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
