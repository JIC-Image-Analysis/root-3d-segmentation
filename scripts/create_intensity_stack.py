"""Create stack where each cell is coloured by normalised intensity."""

import argparse
import json

import os
import os.path

from jicbioimage.core.image import Image3D
from jicbioimage.core.io import AutoName
from jicbioimage.illustrate import Canvas


def normalised_intensity(cell_props):
    """Return the normalised intensity from a cell info entry."""
    return float(cell_props["intensity"]) / cell_props["area"]


def min_max_normalised_intenisty(cellinfo):
    """Return (min, max) normalised intensity tuple."""
    normalised_intensities = [normalised_intensity(p) for p in cellinfo]
    return min(normalised_intensities), max(normalised_intensities)


def get_rgb_from_normalised_intensity(normalised_intensity, imin, imax):
    green = ((normalised_intensity - imin) / (imax - imin)) * 255
    return (0, green, 255)


def write_zslice(zslice, cellinfo, fpath):
    """Write PNG z-slice."""
    ydim, xdim = zslice.shape
    imin, imax = min_max_normalised_intenisty(cellinfo)
    canvas = Canvas.blank_canvas(width=xdim, height=ydim)
    for props in cellinfo:
        ni = normalised_intensity(props)
        color = get_rgb_from_normalised_intensity(ni, imin, imax)
        region = zslice == props["identifier"]
        canvas.mask_region(region, color)

    with open(fpath, "wb") as fh:
        fh.write(canvas.png())


def create_intensity_stack(cells, cellinfo):
    """Write PNG zslices to stack directory."""

    dpath = AutoName.name(create_intensity_stack)
    dpath = dpath + ".stack"
    if not os.path.isdir(dpath):
        os.mkdir(dpath)

    ydim, xdim, zdim = cells.shape
    for zi in range(zdim):
        write_zslice(cells[:, :, zi],
                     cellinfo,
                     os.path.join(dpath, "z{:02d}.png".format(zi)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        parser.error("No such dir: " + args.input_dir)
    AutoName.directory = args.input_dir

    cellinfo = json.load(file(os.path.join(args.input_dir, "cellinfo.json")))
    cells = Image3D.from_directory(args.input_dir)

    create_intensity_stack(cells, cellinfo)
