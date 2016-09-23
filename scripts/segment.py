"""Code for segmenting 3D images."""

import SimpleITK as sitk

import numpy as np
import skimage.morphology

from jicbioimage.core.image import Image3D
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoWrite

from jicbioimage.transform import (
    threshold_otsu,
    remove_small_objects,
)

from utils import ColorImage3D


@transformation
def identity(im3d):
    return im3d


@transformation
def pseudo_convex_hull(im3d):
    stack = []
    ydim, xdim, zdim = im3d.shape
    for i in range(zdim):
        slice_hull = skimage.morphology.convex_hull_image(im3d[:, :, i])
        stack.append(slice_hull)
    return np.dstack(stack).view(Image3D)


@transformation
def remove_small_objects_in_plane(im3d, min_size):
    tmp_auto_write_on = AutoWrite.on
    AutoWrite.on = False
    stack = []
    ydim, xdim, zdim = im3d.shape
    for i in range(zdim):
        slice_hull = remove_small_objects(im3d[:, :, i], min_size)
        stack.append(slice_hull)

    AutoWrite.on = tmp_auto_write_on
    return np.dstack(stack).view(Image3D)


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
    gaussian_filter.SetVariance(variance)
    itk_im = gaussian_filter.Execute(itk_im)
    return Image3D.from_array(sitk.GetArrayFromImage(itk_im),
                              log_in_history=False)


@transformation
def morphological_watershed(im3d, level):
    itk_im = sitk.GetImageFromArray(im3d)
    itk_im = sitk.MorphologicalWatershed(itk_im, level=level)
    return ColorImage3D.from_array(sitk.GetArrayFromImage(itk_im),
                                   log_in_history=False)


@transformation
def filter_cells_outside_mask(im3d, mask):
    inverse_mask = np.logical_not(mask)
    ids_to_filter = np.unique(im3d * inverse_mask)
    for i in ids_to_filter:
        im3d[im3d == i] = 0
    return im3d


@transformation
def remove_border_segmentations(im3d):
    """Remove segments that touch the image border."""
    ydim, xdim, zdim = im3d.shape

    # Identify any segments that touch the image border.
    border_seg_ids = set()
    border_seg_ids.update(set(np.unique(im3d[0, :, :])))
    border_seg_ids.update(set(np.unique(im3d[:, 0, :])))
    border_seg_ids.update(set(np.unique(im3d[ydim-1, :, :])))
    border_seg_ids.update(set(np.unique(im3d[:, xdim-1, :])))

    # Remove those segments.
    for i in border_seg_ids:
        im3d[im3d == i] = 0

    return im3d


def segment(stack):
    """Segment the stack into 3D regions representing cells."""
    mask = threshold_otsu(stack)
    mask = remove_small_objects_in_plane(mask, min_size=1000)
    mask = pseudo_convex_hull(mask)
    stack = identity(stack)
    stack = filter_median(stack)
    stack = gradient_magnitude(stack)
    stack = discrete_gaussian_filter(stack, 2.0)
    stack = morphological_watershed(stack, 0.664)
    stack = filter_cells_outside_mask(stack, mask)
    stack = remove_border_segmentations(stack)
    return stack
