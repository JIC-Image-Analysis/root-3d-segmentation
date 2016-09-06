"""Find regions that correspond to cells."""

import os
import os.path
import argparse
import json

from utils import ColorImage3D


def filter_by_property(im3d, cellinfo, filter_func, min_size, max_size):
    new_cellinfo = []
    for props in cellinfo:
        if not filter_func(props, min_size, max_size):
            im3d[im3d == props["cell_id"]] = 0
        else:
            new_cellinfo.append(props)
    return im3d, new_cellinfo


def real_cells(cell_properties, min_size, max_size):
    if cell_properties["voxels"] < min_size:
        return False
    if cell_properties["voxels"] > max_size:
        return False
    return True


def main(input_dir, output_dir, min_size, max_size):
    cellinfo = json.load(file(os.path.join(input_dir, "cellinfo.json")))
    cells = ColorImage3D.from_directory(input_dir)

    cells, cellinfo = filter_by_property(cells, cellinfo, real_cells,
                                         min_size=min_size,
                                         max_size=max_size)

    cells.to_directory(output_dir)
    with open(os.path.join(output_dir, "cellinfo.json"), "w") as fh:
        json.dump(cellinfo, fh, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--min_size", type=int, default=10000)
    parser.add_argument("--max_size", type=int, default=80000)
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        parser.error("No such dir: " + args.input_dir)

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    main(args.input_dir, args.output_dir, args.min_size, args.max_size)
