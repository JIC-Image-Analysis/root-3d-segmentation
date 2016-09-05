"""Module for returning information about individual cells."""

import numpy as np


def find_summed_intensity_per_cell(intensity_stack, segmentation):
    """Return dictionary in which keys are region identifiers and values are
    summed voxel intensities taken from intensity_stack."""

    summed_intensities = {}

    for i in segmentation.identifiers:
        region_coords = segmentation.region_by_identifier(i).index_arrays
        value = int(np.sum(intensity_stack[region_coords]))
        summed_intensities[str(i)] = dict(intensity=value)

    return summed_intensities


def cellinfo(intensity_stack, segmented_stack):
    """Return list of dictionaries with cell information."""
    summary_data = find_summed_intensity_per_cell(intensity_stack,
                                                  segmented_stack)

    for identifier in segmented_stack.identifiers:
        segment = segmented_stack.region_by_identifier(identifier)
        area = int(segment.area)
        centroid = map(float, segment.centroid)

        datum = {"area": area,
                 "centroid": centroid,
                 "identifier": int(identifier)}
        summary_data[str(identifier)].update(datum)

    return summary_data.values()
