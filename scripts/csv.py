"""Module for producing CSV output."""

import os.path
import argparse
import json

COLUMNS = ("file",
           "series_name",
           "series_id",
           "cell_id",
           "voxels",
           "total_intensity",
           "x",
           "y",
           "z")


def header():
    return ",".join(COLUMNS)


def row(fname, series_name, series_id, cell):
    cell["file"] = fname
    cell["series_name"] = series_name
    cell["series_id"] = series_id

    # Split centroid into x, y, z.
    y, x, z = cell["centroid"]
    del cell["centroid"]
    cell["x"] = x
    cell["y"] = y
    cell["z"] = z

    values = [str(cell[k]) for k in COLUMNS]
    return ','.join(values)


def csv(fname, series_name, series_id, cellinfo):
    lines = []
    for cell in cellinfo:
        lines.append(row(fname, series_name, series_id, cell))
    return "\n".join(lines)
