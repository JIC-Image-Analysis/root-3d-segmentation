"""Code for segmenting 3D images."""

import os.path

import SimpleITK as sitk

from jicbioimage.core.image import Image, Image3D
from jicbioimage.core.util.array import unique_color_array
from jicbioimage.core.transform import transformation

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
    return ColorImage3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


def segment(stack):
    """Segment the stack into 3D regions representing cells."""
    stack = identity(stack)
    stack = filter_median(stack)
    stack = gradient_magnitude(stack)
    stack = discrete_gaussian_filter(stack, 2.0)
    stack = morphological_watershed(stack, 250)
    return stack
