"""Find regions that correspond to cells."""

import os
import os.path
import argparse
import json

from jicbioimage.core.io import AutoName

from utils import ColorImage3D


def filter_by_property(im3d, cellinfo, filter_func):
    new_cellinfo = []
    for props in cellinfo:
        if not filter_func(props):
            im3d[im3d == props["identifier"]] = 0
        else:
            new_cellinfo.append(props)

    dpath = AutoName.name(filter_by_property)
    dpath = dpath + ".info.stack"
    if not os.path.isdir(dpath):
        os.mkdir(dpath)

    im3d.to_directory(dpath)
    with open(os.path.join(dpath, "cellinfo.json"), "w") as fh:
        json.dump(new_cellinfo, fh, indent=2)

    return im3d


def real_cells(cell_properties):
    if cell_properties["area"] < 10000:
        return False
    if cell_properties["area"] > 80000:
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        parser.error("No such dir: " + args.input_dir)
    AutoName.directory = args.input_dir

    cellinfo = json.load(file(os.path.join(args.input_dir, "cellinfo.json")))
    cells = ColorImage3D.from_directory(args.input_dir)

    cells = filter_by_property(cells, cellinfo, real_cells)
