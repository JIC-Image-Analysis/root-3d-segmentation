"""Utility functions."""

import os

import numpy as np
import skimage.io

from jicbioimage.core.util.array import unique_color_array, pretty_color_array
from jicbioimage.core.util.color import identifier_from_unique_color
from jicbioimage.core.image import _sorted_listdir, Image, Image3D

class PrettyColorImage3D(Image3D):
    def to_directory(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        xdim, ydim, zdim = self.shape
        num_digits = Image3D._num_digits(zdim-1)
        for z in range(zdim):
            num = str(z).zfill(num_digits)
            fname = "z{}.png".format(num)
            fpath = os.path.join(directory, fname)
            with open(fpath, "wb") as fh:
                im = Image.from_array(pretty_color_array(self[:, :, z]))
                fh.write(im.png())

class ColorImage3D(Image3D):
    def to_directory(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        xdim, ydim, zdim = self.shape
        num_digits = Image3D._num_digits(zdim-1)
        for z in range(zdim):
            num = str(z).zfill(num_digits)
            fname = "z{}.png".format(num)
            fpath = os.path.join(directory, fname)
            with open(fpath, "wb") as fh:
                im = Image.from_array(unique_color_array(self[:, :, z]))
                fh.write(im.png())

    @staticmethod
    def _rgb_to_identifier(array):
        ydim, xdim, zdim = array.shape
        id_array = np.zeros((ydim, xdim), dtype=np.uint64)

        for y in range(ydim):
            for x in range(xdim):
                id_array[y, x] = identifier_from_unique_color(array[y, x])

        return id_array

    @classmethod
    def from_directory(cls, directory):
        skimage.io.use_plugin('freeimage')

        def is_image_fname(fname):
            "Return True if fname is '.png', '.tif' or '.tiff'."""
            image_exts = set([".png", ".tif", ".tiff"])
            base, ext = os.path.splitext(fname)
            return ext in image_exts
        fnames = [fn for fn in _sorted_listdir(directory)
                  if is_image_fname(fn)]
        fpaths = [os.path.join(directory, fn) for fn in fnames]

        images = [cls._rgb_to_identifier(skimage.io.imread(fp))
                  for fp in fpaths]
        stack = np.dstack(images)
        return stack.view(cls)
