"""Create stack where each cell is coloured by normalised intensity."""

import argparse
import json

import numpy as np

import os
import os.path

from jicbioimage.core.io import AutoName
from jicbioimage.illustrate import Canvas

from utils import ColorImage3D


def intensity_per_volume(cell_props):
    """Return the intensity per volume for a cell."""
    return float(cell_props["total_intensity"]) / cell_props["voxels"]


def min_max_cell_intensity(cellinfo):
    """Return (min, max) cell intensity tuple."""
    cell_intensities = [intensity_per_volume(p) for p in cellinfo]
    return min(cell_intensities), max(cell_intensities)


def get_normalised_rgb_from_cell_intensity(cell_intensity, imin, imax):
    green = ((cell_intensity - imin) / (imax - imin)) * 255
    green = int(round(green))
    assert green >= 0
    assert green < 256
    return (green, green, 255 - green)


def write_zslice(zslice, cellinfo, fpath):
    """Write PNG z-slice."""
    ydim, xdim = zslice.shape
    imin, imax = min_max_cell_intensity(cellinfo)
    canvas = Canvas.blank_canvas(width=xdim, height=ydim)
    for i, props in enumerate(cellinfo):
        cell_intenistity = intensity_per_volume(props)
        color = get_normalised_rgb_from_cell_intensity(cell_intenistity,
                                                       imin, imax)
        region = zslice == props["cell_id"]
        if np.sum(region) == 0:
            continue
        canvas.mask_region(region, color)

    with open(fpath, "wb") as fh:
        fh.write(canvas.png())


def create_intensity_stack(cells, cellinfo, output_dir):
    """Write PNG zslices to stack directory."""
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    ydim, xdim, zdim = cells.shape
    for zi in range(zdim):
        write_zslice(cells[:, :, zi],
                     cellinfo,
                     os.path.join(output_dir, "z{:02d}.png".format(zi)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        parser.error("No such dir: " + args.input_dir)

    cellinfo = json.load(file(os.path.join(args.input_dir, "cellinfo.json")))
    cells = ColorImage3D.from_directory(args.input_dir)

    create_intensity_stack(cells, cellinfo, args.output_dir)
