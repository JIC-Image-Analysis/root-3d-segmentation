"""Code for segmenting 3D images."""

import SimpleITK as sitk

from jicbioimage.core.image import Image3D
from jicbioimage.core.transform import transformation

from utils import ColorImage3D


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
